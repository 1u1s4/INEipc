import requests
import json
from funcionesjo import year_ago, month_after, date_mini, mes_by_ordinal, hoy
import descriptor

FECHA_REPORTE = "2015-10-01"#hoy("%Y-%m-%d")
FECHA_ANTERIOR = year_ago(FECHA_REPORTE)
FECHA_ANTERIOR_ANTERIOR = year_ago(FECHA_ANTERIOR)
API_KEY = "515963d6-1153-e348-8394-a81acec0d6da"
#Llamado al API
URL = f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/628222/es/0700/false/BIE/2.0/{API_KEY}?type=json'
response= requests.get(URL)
data = {}
if response.status_code == 200:
    content = json.loads(response.content)
    series = content["Series"]
    for i in series[0]["OBSERVATIONS"]:
        marca_temporal = "-".join(i["TIME_PERIOD"].split("/")[0:2])
        data[marca_temporal] = float(i["OBS_VALUE"])
# ya una vez cargada la informacion se hace la tasa de variacion
fecha_i = FECHA_ANTERIOR
datos_variacion_interanual = []
for i in range(13):
    precio = data[date_mini(fecha_i)]
    precio_anterior = data[date_mini(year_ago(fecha_i))]
    mes_actual_i = "-".join((fecha_i.split("-")[0], mes_by_ordinal(fecha_i.split("-")[1])))
    variacion = ((precio / precio_anterior) - 1) * 100
    datos_variacion_interanual.append((mes_actual_i, variacion))

    fecha_i = month_after(fecha_i)

for i in datos_variacion_interanual:
    print(i)
print(descriptor.ipc_mex(datos_variacion_interanual))