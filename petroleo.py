from fredapi import Fred
from datetime import datetime, timedelta
from datetimeLAAR import year_ago, month_after, date_mini, mes_by_ordinal
fred = Fred(api_key='734b605521e7734edc09f38e977fe238')
FECHA_REPORTE = "2015-11-22"#datetime.today().strftime("%Y-%m-%d")
FECHA_ANTERIOR = year_ago(FECHA_REPORTE)
# carga de datos
data = fred.get_series('DCOILWTICO', observation_start=FECHA_ANTERIOR, observation_end=FECHA_REPORTE)
# extraccion de los datos en el rango de fechas
fecha_i = FECHA_ANTERIOR
mes_actual = "-".join((fecha_i.split("-")[0], mes_by_ordinal(fecha_i.split("-")[1])))
datos_mes = []
data_mean = []
while fecha_i != FECHA_REPORTE:
    fecha_i = datetime.strptime(fecha_i, "%Y-%m-%d") + timedelta(days=1)
    fecha_i = fecha_i.strftime("%Y-%m-%d")
    mes_actual_i = "-".join((fecha_i.split("-")[0], mes_by_ordinal(fecha_i.split("-")[1])))
    if mes_actual_i != mes_actual:
        mean = sum(datos_mes)/len(datos_mes)
        data_mean.append((mes_actual, f"{mean:.2f}"))
        datos_mes = []
        mes_actual = mes_actual_i
    try:
        precio = data.dropna().loc[fecha_i]
        datos_mes.append(precio)
    except Exception as e:
        None
for i in data_mean:
    print(i)