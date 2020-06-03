#!/bin/bash
for year in 2018 2019
do
  for month in {1..12}
  do
    for day in {1..28}
    do
    if [ ${#day} -eq 1 ]
    then
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-0$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-0$day
      fi
    else
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-$day
      fi
    fi 
    done
  done
done

for year in 2018 2019
do
  for month in 4 6 9 11
  do
    for day in 29 30
    do
    if [ ${#day} -eq 1 ]
    then
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-0$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-0$day
      fi
    else
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-$day
      fi
    fi 
    done
  done
done


for year in 2018 2019
do
  for month in 1 3 5 7 8 10 12
  do
    for day in 29 30 31
    do
    if [ ${#day} -eq 1 ]
    then
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-0$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-0$day
      fi
    else
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-$day
      fi
    fi 
    done
  done
done

for year in 2020
do
  for month in 1 2
  do
    for day in {1..29}
    do
    if [ ${#day} -eq 1 ]
    then
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-0$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-0$day
      fi
    else
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-$day
      fi
    fi 
    done
  done
done

for year in 2020
do
  for month in 1
  do
    for day in 30 31
    do
    if [ ${#day} -eq 1 ]
    then
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-0$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-0$day
      fi
    else
      if [ ${#month} -eq 1 ]
      then
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-0$month-$day
      else
        python3 -m luigi --module get_api_data_new copyToPostgres  --scheduler-host localhost --bucket test-aws-gab --date $year-$month-$day
      fi
    fi 
    done
  done
done
