import requests
import json
from datetime import datetime, timedelta
from datetimeLAAR import year_ago, month_after, date_mini
FECHA_REPORTE = "2015-10-01"#datetime.today().strftime("%Y-%m-%d")
FECHA_ANTERIOR = year_ago(FECHA_REPORTE)
FECHA_ANTERIOR_ANTERIOR = year_ago(FECHA_ANTERIOR)
MES_FORMATO = {
    "01":"Ene",
    "02":"Feb",
    "03":"Mar",
    "04":"Abr",
    "05":"May",
    "06":"Jun",
    "07":"Jul",
    "08":"Ago",
    "09":"Sep",
    "10":"Oct",
    "11":"Nov",
    "12":"Dic"
}
API_KEY = "515963d6-1153-e348-8394-a81acec0d6da"
#Llamado al API
url=f'  https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/628222/es/0700/false/BIE/2.0/{API_KEY}?type=json'
response= requests.get(url)
data = {}
if response.status_code==200:
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
    mes_actual_i = "-".join((fecha_i.split("-")[0], MES_FORMATO[fecha_i.split("-")[1]]))
    variacion = ((precio / precio_anterior) - 1) * 100
    datos_variacion_interanual.append((mes_actual_i, f"{variacion:.2f}"))

    fecha_i = month_after(fecha_i)

for i in datos_variacion_interanual:
    print(i)
