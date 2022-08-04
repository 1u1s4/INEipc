from fredapi import Fred
from funcionesjo import year_ago, anio_mes, mes_by_ordinal, hoy, day_after

def petroleo(fecha_hasta="", fecha_desde="") -> list[tuple]:
    FORMATO = "%Y-%m-%d"
    API_KEY ='734b605521e7734edc09f38e977fe238'
    SERIES_ID = 'DCOILWTICO'
    fred = Fred(api_key=API_KEY)
    if len(fecha_hasta) == 0:
        FECHA_REPORTE = hoy(FORMATO)
    else:
        FECHA_REPORTE = fecha_hasta
    if len(fecha_desde) == 0:
        FECHA_ANTERIOR = year_ago(fecha=FECHA_REPORTE)
    else:
        FECHA_ANTERIOR = fecha_desde
    # carga de datos
    data = fred.get_series(
        series_id=SERIES_ID,
        observation_start=FECHA_ANTERIOR,
        bservation_end=FECHA_REPORTE
    )
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
        except:
            None
    return data_mean
