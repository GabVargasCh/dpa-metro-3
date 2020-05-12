# dpa-metro-cdmx

## Introduccion 

El Metro es el principal sistema de transporte que conecta a la ciudad mediante trenes subterráneos y superficiales organizados en 12 líneas con 195 estaciones en diferentes rutas a traves de 200.88 km de vias. Cuenta con 3213 vagones que movilizaron en 2018 a 1,647 millones diarios en 2018 segun cifras de operacion de la ciudad. No hay datos puntuales de las anomalias o de cuando sufre una sobredemanda el sistema pero de acuerdo con datos operacionales de la cdmx [https://www.metro.cdmx.gob.mx/storage/app/media/Banners/diagnostico.pdf] esto ocurre con bastante frecuencia.

Dada la cantidad de anomaias y fallas en el sistema de transporte de la ciudad, podemos plantear la pregunta de si ¿el sistema es un sitema inteligente? Y si al viajar en el sistema  el usuario ¿tiene una experiencia inteligente?

Probablemente la respuesta es que no, y para ayudar a contruir una experiencia y un sistema asi contamos con los datos de la afluencia diaria por estacion desde 2015. 

## Descripcion de los datos

Utilizaremos los de Afluencia diaria del Metro CDMX del datos del portal de datos de la ciudad de Mexico [datos de la Ciudad](https://datos.cdmx.gob.mx) Esta base muestra la afluencia diaria del Metro CDMX. Los datos abarcan de enero de 2010 a febrero de 2020 y se actualiza mensualmente. Para adquirirlos utilizaremos la API del sitio, de donde los extraeremos como json con los siguientes campos.

- "anio":"2018",
- "estacion":"Balbuena",
- "fecha":"2018-01-01",
- "linea":"Linea 1",
- "afluencia":"3739"

Mas metadata. 

## Planteamiento del problema

A partir de los datos que tenemos, sería muy ambicioso construir un sistema de mantenimiento predictivo o incluso una solución que informe a la población en que momento del dia y que dia el sistema estara saturado. Sin embargo podemos tener listo al sistema para cuando este saturado. Estos efectos pueden ser locales, es decir puede haber un concierto que sature alguna estacion en particular mientras que toda la red este subutilizada (personal de limpieza, vagones, taquilleros, personal de seguridad, choferes, personal de mantenimiento, personal de asistencia a personas con discapacidad). Es por esto que nuestras principales dos preguntas seran.

- ¿ Cuando estara saturada una estacion?
- ¿ Cual es la estacion mas cercana que no esta saturada?

Si logramos resolver estas dos preguntas sencillas con una solucion compleja y robusta podremos ayudar a movilizar al personal de las estaciones cercanas subutilizadas a aquellas que van a saturarse. Para resolver las preguntas realizaremos un producto de datos para personas. Que colecte de forma automatica cada mes los datos y genere una prescripcion a las personas responsables de movilizar los recursos de personal dentro del sistema de trasnporte colectivo

## Implicaciones eticas

Al realizar un modelo predictivo debemos tener en cuenta que estamos haciendo estimaciones y son sensibles al error. Por eso es muy importante hacer un monitoreo online y offline de nuestro modelo. Es decir ver en batch las tasas de error por arriba y por abajo. El hecho de estimar mas afluencia de la real impactaria en la movilizacion de personal (costos y tiempo) y en quitar personal a una estacion (aunque en principio no lo necesitaria). Pero estimar por abajo la afluencia de una estacion puede afectar a cientos de miles de usuarios ya que posiblemente desplazariamos al personal a otra estacion incurriendo en costos y en afectaciones al servicio. Por lo que sera importante cuidar mas el error por abajo.

### Metricas de fairness y atributos protegidos

Estas predicciones pueden llevar a que hagamos desplacemos el personal de una estacion hacia otra de forma mas constante si estimamos constantemente por abajo la afluencia de alguna estacion. Entonces cuando la afluencia sea baja la denominaremos como un negativo y cuando sea mas alta como un positivo. Entonces.

- Afluencia alta, Estimada como alta: verdadero positivo
- Afluencia baja, Estimada como alta: falso positivo
- Afluencia baja, Estimada como baja: verdadero negativo
- Afluencia alta, Estimada como baja: falso negativo

Con estas definiciones podemos ver que lo que mas afectaria serian los **falsos negativos** pues estariamos estimando menos afluencia a la real y posiblemente movilizariamos al personal de esa estacion. Una de las variables perjudicadas puede ser la linea o la estacion mas cercana. Es decir si hay lineas que se ven mas afectadas que otras en su **FNR**. Por otra parte si para la variable *estacion mas cercana* puede ser que haya alguna que este presente cuando hay mayor **FPR** que para las demas entonces. Entonces esas estaciones se pueden ver afectadas ya que si para su estacion vecina estamos estimando mayor afluencia de la habitual, la accion es desplazar personal de la estacion mas cercana y puede ser que la perjudiquemos constantemente o en mayor medida que las demas y tener un sesgo con implicaciones eticas. Por ello tenemos que tomar la variable *linea* y *nearest_station* como atributos protegidos.
















http://cdmxtravel.com/es/organizate/como-moverse/sistema-de-transporte-colectivo-metro.html

https://link.springer.com/book/10.1007/978-1-4842-3432-7

https://metro.cdmx.gob.mx/operacion/cifras-de-operacion
