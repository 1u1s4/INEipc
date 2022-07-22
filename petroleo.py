from fredapi import Fred
import numpy as np
from datetime import datetime, timedelta
fred = Fred(api_key='734b605521e7734edc09f38e977fe238')
FECHA_REPORTE = "2015-11-22"#datetime.today().strftime("%Y-%m-%d")
FECHA_ANTERIOR = "-".join((str(int(FECHA_REPORTE.split("-")[0]) - 1), FECHA_REPORTE.split("-")[1], "01"))
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
data = fred.get_series('DCOILWTICO', observation_start=FECHA_ANTERIOR, observation_end=FECHA_REPORTE)
fecha_i = FECHA_ANTERIOR
mes_actual = "-".join((fecha_i.split("-")[0], MES_FORMATO[fecha_i.split("-")[1]]))
datos_mes = []
data_mean = []
while fecha_i != FECHA_REPORTE:
    fecha_i = datetime.strptime(fecha_i, "%Y-%m-%d") + timedelta(days=1)
    fecha_i = fecha_i.strftime("%Y-%m-%d")
    mes_actual_i = "-".join((fecha_i.split("-")[0], MES_FORMATO[fecha_i.split("-")[1]]))
    if mes_actual_i != mes_actual:
        data_mean.append((mes_actual, sum(datos_mes)/len(datos_mes)))
        datos_mes = []
        mes_actual = mes_actual_i
    try:
        precio = data.dropna().loc[fecha_i]
        datos_mes.append(precio)
    except Exception as e:
        None
for i in data_mean:
    print(i)