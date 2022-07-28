from fredapi import Fred
from datetime import datetime, timedelta
from datetimeLAAR import year_ago, month_after
fred = Fred(api_key='734b605521e7734edc09f38e977fe238')
FECHA_REPORTE = "2022-06-01"#datetime.today().strftime("%Y-%m-%d")
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
data = fred.get_series('CPIAUCSL', observation_start=FECHA_ANTERIOR_ANTERIOR, observation_end=FECHA_REPORTE)
fecha_i = FECHA_ANTERIOR
datos_variacion_interanual = []
for i in range(13):
    precio = data.dropna().loc[fecha_i]
    precio_anterior = data.dropna().loc[year_ago(fecha_i)]
    mes_actual_i = "-".join((fecha_i.split("-")[0], MES_FORMATO[fecha_i.split("-")[1]]))
    variacion = ((precio / precio_anterior) - 1) * 100
    datos_variacion_interanual.append((mes_actual_i, f"{variacion:.2f}"))

    fecha_i = month_after(fecha_i)

for i in datos_variacion_interanual:
    print(i)
