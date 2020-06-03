# existe un bug con bot3 y luigi para pasar las credenciales
# necesitas enviar el parametro AWS_PROFILE e indicar el profile
# con el que quieres que se corra
# PYTHONPATH='.' AWS_PROFILE=mge luigi --module ex3_luigi S3Task --local-scheduler ...
import requests
import pandas
import json
import luigi
import boto3
import psycopg2
import sys
import pandas as pd
import luigi.contrib.s3
import os
import subprocess
import requests
import pickle
import geopandas
from shapely.ops import nearest_points
import re
import ast
from pylab import rcParams
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LassoLarsCV
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import RFE
import math
import numpy as np
import time
from datetime import datetime as date
from luigi.contrib.postgres import CopyToTable

class extractToJson(luigi.Task):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  def requires(self):
    return None

  def run(self):

    ses = boto3.session.Session(profile_name='gabster', region_name='us-west-2')
    s3_resource = ses.resource('s3')
    obj = s3_resource.Bucket(self.bucket)

    data_raw = requests.get(f"https://datos.cdmx.gob.mx/api/records/1.0/search/?dataset=afluencia-diaria-del-metro-cdmx&rows=10000&sort=-fecha&refine.fecha={self.date}")
    # data_raw.status_code
    # data_raw.headers['content-type']
    # data_raw.headers['Date']
    # data_raw.json()

    with self.output().open('w') as json_file:
      json.dump(data_raw.json(), json_file)

    dt= date.now()

    params = {'Params': [self.task_name, self.date]
        }

    buc = "s3://{}/{}/metro_{}.json".\
        format(self.bucket, self.task_name, self.date)

    md = {'Date': [str(dt)], 'Params': [params],'Bucket': [buc]
        }

    df = pd.DataFrame(md, columns = ['Date','Params', 'Bucket'])

    df.to_csv('md_extract.csv',index=False)

  def output(self):
    output_path = "s3://{}/{}/metro_{}.json".\
      format(self.bucket, self.task_name, self.date)
    return luigi.contrib.s3.S3Target(path=output_path)

class md_extract(CopyToTable):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  creds = pd.read_csv("credentials_postgres.csv")
  user = creds.user[0]
  password = creds.password[0]
  host = creds.host[0]
  port = creds.port[0]
  database = creds.db[0]
  table = 'md_extract'

  columns = [("Date", "VARCHAR"), 
              ("Params", "VARCHAR"),
              ("Bucket", "VARCHAR")]

  def requires(self):
    return extractToJson(bucket = self.bucket, date = self.date) 

  def rows(self):
    df = pd.read_csv("md_extract.csv")
    t= [tuple(x) for x in df.to_records(index=False)] 
    for tup in t:
        yield tup

class ut_extract(luigi.Task):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  def requires(self):
    return md_extract(bucket = self.bucket, date = self.date)

  def output(self):
        return luigi.LocalTarget("ute.txt") 

  def run(self):
    subprocess.call(['./extract_data_utest.sh'])
    with self.output().open('w') as output_file:
      z = "succesful"
      output_file.write(z)

class loadToPostgres(luigi.Task):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  def requires(self):
    return ut_extract(bucket = self.bucket, date = self.date)

  def output(self):
    return luigi.LocalTarget('md_load.csv')

  def run(self):
    file_to_read = self.task_name+'/metro_'+self.date+'.json'
    creds = pd.read_csv("credentials_postgres.csv")
    creds_aws = pd.read_csv("credentials.csv")
    s3 = boto3.resource('s3', aws_access_key_id=creds_aws.Access_key_ID[0],aws_secret_access_key=creds_aws.Secret_access_key[0])
    content_object = s3.Object(self.bucket, file_to_read)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)

    df = pd.DataFrame(columns=["fecha", "anio", "linea", "estacion", "afluencia"])

    for i in range(len(json_content['records'])):
      a_row = pd.Series([json_content['records'][i]["fields"]["fecha"], json_content['records'][i]["fields"]["anio"],json_content['records'][i]["fields"]["linea"], json_content['records'][i]["fields"]["estacion"],int(json_content['records'][i]["fields"]["afluencia"])])
      row_df = pd.DataFrame([a_row])
      row_df.columns = ["fecha", "anio", "linea", "estacion", "afluencia"]
      df = pd.concat([df, row_df], ignore_index=True)
    connection = psycopg2.connect(user = creds.user[0],
    password = creds.password[0],
    host = creds.host[0],
    port = creds.port[0],
    database = creds.db[0])
    cursor = connection.cursor()
    for i in df.index:
      text = "INSERT INTO raw  VALUES ('%s', '%s', '%s', '%s', %d);" %(df["fecha"][i], df["anio"][i], df["linea"][i], df["estacion"][i], df["afluencia"][i])
      print(text)
      cursor.execute(text)
    connection.commit()
    cursor.close()
    connection.close()

    dt= date.now()
    name= "raw"
    database = creds.db[0]
    md = {'Date': [str(dt)],'Table_name': [name], 'DB': [database]}
    df = pd.DataFrame(md, columns = ['Date','Table_name','DB'])
    df.to_csv('md_load_h.csv',index=False)

    with self.output().open('w') as output_file:
      df.to_csv(output_file, index=False)

class md_load(CopyToTable):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  creds = pd.read_csv("credentials_postgres.csv")
  user = creds.user[0]
  password = creds.password[0]
  host = creds.host[0]
  port = creds.port[0]
  database = creds.db[0]
  table = 'md_load'

  columns = [("Date", "VARCHAR"), 
              ("Table_name", "VARCHAR"),
              ("DB", "VARCHAR")]

  def requires(self):
    return loadToPostgres(bucket = self.bucket, date = self.date) 

  def rows(self):
    df = pd.read_csv("md_load_h.csv")
    t= [tuple(x) for x in df.to_records(index=False)] 
    for tup in t:
        yield tup

class ut_load(luigi.Task):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  def requires(self):
    return md_load(bucket = self.bucket, date = self.date)

  def output(self):
    return luigi.LocalTarget("utl.txt") 

  def run(self):
    subprocess.call(['./load_data_utest.sh'])
    with self.output().open('w') as output_file:
      z = "succesful"
      output_file.write(z)

class md_ut_load(CopyToTable):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  creds = pd.read_csv("credentials_postgres.csv")
  user = creds.user[0]
  password = creds.password[0]
  host = creds.host[0]
  port = creds.port[0]
  database = creds.db[0]
  table = 'md_ut_load'

  columns = [("Test", "VARCHAR"), 
              ("Timestamp", "VARCHAR"),
              ("Status", "VARCHAR"),
              ("Runtime", "VARCHAR")]

  def requires(self):
    return ut_load(bucket = self.bucket, date = self.date) 

  def rows(self):
    df = pd.read_csv("md_ut_load.csv")
    t= [tuple(x) for x in df.to_records(index=False)] 
    for tup in t:
        yield tup

class modelling(luigi.Task):
  task_name = 'raw_json'
  date = luigi.Parameter()
  bucket = luigi.Parameter()

  def requires(self):
    return md_ut_load(bucket = self.bucket, date = self.date)

  def output(self):
    return luigi.LocalTarget("fe.txt") 

  def run(self):
    subprocess.call(['./modelling_complete.sh'])
    with self.output().open('w') as output_file:
      z = "succesful"
      output_file.write(z)









