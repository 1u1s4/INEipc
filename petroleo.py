from fredapi import Fred
from funcionesjo import year_ago, anio_mes, mes_by_ordinal, hoy, day_after


import descriptor
fred = Fred(api_key='734b605521e7734edc09f38e977fe238')
FORMATO = "%Y-%m-%d"
FECHA_REPORTE = "2015-11-01"#hoy(FORMATO)
FECHA_ANTERIOR = year_ago(FECHA_REPORTE)
# carga de datos
data = fred.get_series('DCOILWTICO', observation_start=FECHA_ANTERIOR, observation_end=FECHA_REPORTE)
# extraccion de los datos en el rango de fechas
fecha_i = FECHA_ANTERIOR
mes_actual = "-".join((fecha_i.split("-")[0], mes_by_ordinal(fecha_i.split("-")[1])))
datos_mes = []
data_mean = []
while fecha_i != FECHA_REPORTE:
    fecha_i = day_after(fecha_i)
    mes_actual_i = anio_mes(fecha_i)
    if mes_actual_i != mes_actual or fecha_i == FECHA_REPORTE:
        mean = sum(datos_mes) / len(datos_mes)
        data_mean.append((mes_actual, mean))
        datos_mes = []
        mes_actual = mes_actual_i
    try:
        precio = data.dropna().loc[fecha_i]
        datos_mes.append(precio)
    except Exception as e:
        None
for i in data_mean:
    print(i)
print(descriptor.petroleo(data_mean))