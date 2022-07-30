from numpy import var
from datetimeLAAR import mes_anio_by_abreviacion

def variacion(dato: float, dato_antes: float) -> float:
    return ((dato - dato_antes) / dato_antes) * 100
# petroleo
"""
ejemplo de datos
('2014-Nov', '72.36')
('2014-Dic', '59.29')
...
('2015-Sep', '45.48')
('2015-Oct', '46.22')
('2015-Nov', '43.10')
"""
def petroleo(datos: list[tuple[str]]) -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0])
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0])
    FECHA_3 = mes_anio_by_abreviacion(datos[-2][0])
    PRECIO = datos[-1][1]
    DIFERANCIA_1 = datos[-1][1] - datos[0][1]
    VARIACION_1 = variacion(datos[-1][1], datos[0][1])
    if DIFERANCIA_1 > 0:
        SIGNO_1 = ""
    else:
        DIFERANCIA_1 = DIFERANCIA_1 * -1
        SIGNO_1 = "-"
    DIFERANCIA_2 = datos[-1][1] - datos[-2][1]
    VARIACION_2 = variacion(datos[-1][1], datos[-2][1])
    if DIFERANCIA_2 > 0:
        SIGNO_2 = ""
    else:
        DIFERANCIA_2 = DIFERANCIA_2 * -1
        SIGNO_2 = "-"
    PLANTILLA = f"""El precio internacional del petróleo registró en {FECHA_1}
                un precio medio de US${PRECIO:.2f} por barril, lo que representa
                una variación de {VARIACION_1:.2f}% ({SIGNO_1}US${DIFERANCIA_1:.2f})
                respecto a {FECHA_2} y de {VARIACION_2:.2f}% ({SIGNO_2}US${DIFERANCIA_2:.2f}) respecto a {FECHA_3}.
                """
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA

# cambio del quetzal
"""
ejemplo de datos
('2021-Jul', '7.75')
('2021-Ago', '7.74')
...
('2022-Jun', '7.74')
('2022-Jul', '7.74')
"""
def cambio_del_quetzal(datos: list[tuple[str]]) -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0])
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0])
    FECHA_3 = mes_anio_by_abreviacion(datos[-2][0])
    PRECIO = datos[-1][1]
    VARIACION_1 = variacion(datos[-1][1], datos[0][1])
    VARIACION_2 = variacion(datos[-1][1], datos[-2][1])
    PLANTILLA = f"""El tipo de cambio de referencia del
                quetzal respecto al dólar de los Estados
                Unidos de América, registró en {FECHA_1} 
                un precio medio de Q{PRECIO} por
                US$1.00, lo que representa una variación
                de {VARIACION_1:.2f}% respecto a {FECHA_2} y de
                {VARIACION_2:.2f}% respecto a {FECHA_3}."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA