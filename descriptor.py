from funcionesjo import mes_anio_by_abreviacion


def variacion(dato: float, dato_antes: float) -> float:
    return ((dato - dato_antes) / dato_antes) * 100
# petroleo
"""
ejemplo de datos
('2014-Nov', 75.78947368421052)
('2014-Dic', 59.29045454545455)
...
('2015-Sep', 45.479523809523805)
('2015-Oct', 46.22363636363636)
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
('2021-Ago', 7.738385161290321)
...
('2022-Jun', 7.735068333333335)
('2022-Jul', 7.739475806451614)
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
                un precio medio de Q{PRECIO:.2f} por
                US$1.00, lo que representa una variación
                de {VARIACION_1:.2f}% respecto a {FECHA_2} y de
                {VARIACION_2:.2f}% respecto a {FECHA_3}."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA

# tasa de interes
"""
('2021-Ago', 12.139999999999999)
('2021-Sep', 12.16)
...
('2022-Abr', 11.93)
('2022-May', 11.940000000000001)
('2022-Jun', 11.98)
"""
def tasa_de_interes(datos: list[tuple[str]]) -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0])
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0])
    FECHA_3 = mes_anio_by_abreviacion(datos[-2][0])
    TASA = datos[-1][1]
    DIFERENCIA_1 = datos[-1][1] - datos[0][1]
    DIFERENCIA_2 = datos[-1][1] - datos[-2][1]
    if DIFERENCIA_1 < 0:
        CAMBIO_1 = "una disminución"
        DIFERENCIA_1 *= -1
    elif DIFERENCIA_1 > 0:
        CAMBIO_1 = "un aumento"
    else:
        CAMBIO_1 = "un cambio"
    if DIFERENCIA_2 < 0:
        CAMBIO_2 = "una disminución"
        DIFERENCIA_2 *= -1
    elif DIFERENCIA_2 > 0:
        CAMBIO_2 = "un aumento"
    else:
        CAMBIO_2 = "un cambio"
    PLANTILLA = f"""El promedio ponderado preliminar de la tasa de interés activa
    en moneda nacional se ubicó en {FECHA_1} en {TASA:.2f}%, lo que representa
    {CAMBIO_1} de {DIFERENCIA_1:.2f} puntos porcentuales respecto a {FECHA_2}
    y {CAMBIO_2} de {DIFERENCIA_2:.2f} puntos porcentuales respecto a {FECHA_3}."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA

# IPC USA
"""
ejemplo de datos
('2021-Ago', 5.205331689652515)
('2021-Sep', 5.389907375379521)
...
('2022-May', 8.516412942713858)
('2022-Jun', 8.995220608588127)
"""
def ipc_usa(datos: list[tuple[str]]) -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0])
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0])
    INDICE_1 = datos[-1][1]
    INDICE_2 = datos[0][1]
    DIFERENCIA = datos[-1][1] - datos[0][1]
    if DIFERENCIA < 0:
        CAMBIO = "se desaceleró"
        DIFERENCIA *= -1
    elif DIFERENCIA > 0:
        CAMBIO = "se aceleró"
    else:
        CAMBIO = "cambio"
    PLANTILLA = f"""El Índice de Precios al Consumidor en los Estados Unidos de
                América registró una variación interanual al mes de {FECHA_1} de
                {INDICE_1:.2f}%. En {FECHA_2} la variación interanual se ubicó en
                {INDICE_2:.2f}%, por lo que este indicador {CAMBIO} {DIFERENCIA:.2f}
                puntos porcentuales en el último año."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA

# IPC MEX
"""
ejemplo de datos
('2021-Ago', 5.205331689652515)
('2021-Sep', 5.389907375379521)
...
('2022-May', 8.516412942713858)
('2022-Jun', 8.995220608588127)
"""
def ipc_mex(datos: list[tuple[str]]) -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0])
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0])
    INDICE_1 = datos[-1][1]
    INDICE_2 = datos[0][1]
    DIFERENCIA = datos[-1][1] - datos[0][1]
    if DIFERENCIA < 0:
        CAMBIO = "se desaceleró"
        DIFERENCIA *= -1
    elif DIFERENCIA > 0:
        CAMBIO = "se aceleró"
    else:
        CAMBIO = "cambio"
    PLANTILLA = f"""El Índice de Precios al Consumidor en México de registró una
                variación interanual al mes de {FECHA_1} de {INDICE_1:.2f}%. En
                {FECHA_2} la variación interanual se ubicó en {INDICE_2:.2f}%,
                por lo que este indicador {CAMBIO} {DIFERENCIA:.2f} puntos
                porcentuales en el último año."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA
