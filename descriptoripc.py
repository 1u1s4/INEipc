from funcionesjo import mes_anio_by_abreviacion, mes_by_ordinal

def retocar_plantilla(plantilla: str) -> str:
    plantilla = plantilla.replace("\n", " ")
    plantilla = plantilla.split()
    plantilla = " ".join(plantilla)
    return plantilla

def variacion(dato: float, dato_antes: float) -> float:
    return ((dato - dato_antes) / dato_antes) * 100
# indice_precio_alimentos
"""
ejemplo de datos
('2014-Nov', 75.78947368421052)
('2014-Dic', 59.29045454545455)
...
('2015-Sep', 45.479523809523805)
('2015-Oct', 46.22363636363636)
"""
def indice_precio_alimentos(datos: list[tuple[str]]) -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0])
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0])
    FECHA_3 = mes_anio_by_abreviacion(datos[-2][0])
    INDICE = datos[-1][1]
    VARIACION_1 = variacion(datos[-1][1], datos[0][1])
    VARIACION_2 = variacion(datos[-1][1], datos[-2][1])
    PLANTILLA = f"""El índice de precios de los alimentos de la FAO registró en
                {FECHA_1} un índice de {INDICE:.2f}, lo que representa una
                variación de {VARIACION_1:.2f}% respecto a {FECHA_2} y de
                {VARIACION_2:.2f}% respecto a {FECHA_3}."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA
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

def inflacion(datos: dict[dict[str]], fecha: str) -> str:
    MES = mes_by_ordinal(fecha.split("-")[1])
    ANIO = fecha.split("-")[0]
    inflacion_mes = []
    for pais in datos.keys():
        inflacion_mes.append((datos[pais][MES], pais))
    inflacion_mes.sort()
    INFLACION_MIN = inflacion_mes[0]
    INFLACION_MAX = inflacion_mes[-1]
    MES = mes_by_ordinal(fecha.split("-")[1], abreviado=False)
    PLANTILLA = f"""Para el mes de {MES} {ANIO}, en Centro América, República
                Dominicana y México, {INFLACION_MAX[1].capitalize()} presentó
                la mayor tasa de inflación interanual de {INFLACION_MAX[0]:.2f}%,
                mientras que {INFLACION_MIN[1].capitalize()} registró la tasa más
                baja con un nivel de {INFLACION_MIN[0]:.2f}%."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA

def serie_historica_ipc(datos) -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0], MMAA=True)
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
    PLANTILLA = f"""El Índice de Precios al Consumidor registró una
                variación interanual al mes de {FECHA_1} de {INDICE_1:.2f}%. En
                {FECHA_2} la variación interanual se ubicó en {INDICE_2:.2f}%,
                por lo que este indicador {CAMBIO} {DIFERENCIA:.2f} puntos
                porcentuales en el último año."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA
# tipo = intermensual, interanual, acumulada
def serie_historica_inflacion(datos, tipo: str, nivel: str='nacional') -> str:
    FECHA_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
    FECHA_2 = mes_anio_by_abreviacion(datos[0][0], MMAA=True)
    INDICE_1 = datos[-1][1] # mes actual
    INDICE_2 = datos[-2][1] # mes anterior
    INDICE_3 = datos[0][1]
    DIFERENCIA_1 = INDICE_1 - INDICE_2
    DIFERENCIA_2 = INDICE_1 - INDICE_3
    if DIFERENCIA_1 > 0:
        CAMBIO_1 = "un aumento"
    elif DIFERENCIA_1 < 0:
        CAMBIO_1 = "una disminución"
        DIFERENCIA_1 *= -1
    else:
        CAMBIO_1 = "un cambio"
    if DIFERENCIA_2 > 0:
        CAMBIO_2 = "un aumento"
    elif DIFERENCIA_2 < 0:
        CAMBIO_2 = "una disminución"
        DIFERENCIA_2 *= -1
    else:
        CAMBIO_2 = "un cambio"

    PLANTILLA = f"""La variación {tipo} del IPC a nivel {nivel} en {FECHA_1},
                se ubicó en {INDICE_1:.2f}%. Esta variación representa {CAMBIO_1}
                en el nivel de precios de {DIFERENCIA_1:.2f} puntos porcentuales
                respecto al mes anterior ({INDICE_2:.2f}%), y con respecto a la
                variación alcanzada en {FECHA_2} ({INDICE_3:.2f}%) {CAMBIO_2} de
                {DIFERENCIA_2:.2f} puntos."""
    PLANTILLA = PLANTILLA.replace("\n", " ")
    PLANTILLA = PLANTILLA.split()
    PLANTILLA = " ".join(PLANTILLA)
    return PLANTILLA

def incidencia_divisiones(datos, fecha) -> str:
    fecha = mes_anio_by_abreviacion(fecha, MMAA=True)
    datos = sorted(datos, reverse=True)
    mayor_1 = datos[0]
    mayor_2 = datos[1]
    menor = datos[-1]
    div_1 = mayor_1[1].lower()
    div_2 = mayor_2[1].lower()
    div_3 = menor[1].lower()
    indice_menor = menor[0]
    if indice_menor < 0.01 and indice_menor > 0:
        indice_menor = f'{indice_menor:.3f}'
    elif indice_menor < 0.001 and indice_menor > 0:
        indice_menor = f'{indice_menor:.4f}'
    elif indice_menor < 0.0001 and indice_menor > 0:
        indice_menor = f'{indice_menor:.5f}'
    else:
        indice_menor = f'{indice_menor:.2f}'
    plantilla = f"""De las doce divisiones de gasto que integran el IPC, la de
                {div_1} ({mayor_1[0]:.2f}%) y {div_2} ({mayor_2[0]:.2f}%),
                registraron la mayor variación mensual en {fecha}. Por su parte,
                {div_3} es la división de gasto con menor variación mensual
                ({indice_menor}%)."""
    plantilla = plantilla.replace("\n", " ")
    plantilla = plantilla.split()
    plantilla = " ".join(plantilla)
    return plantilla

def incidencias(datos, fecha: str, Qpositivas: bool=True) -> str:
    datos = sorted(datos, reverse=Qpositivas)[0:5]
    if Qpositivas:
        indices = [d[0] for d in datos]
        tipo = 'variaciones'
    else:
        indices = [d[0]*-1 for d in datos]
        tipo = 'variaciones negativas'
    nombres = [d[1].lower() for d in datos]
    plantilla = """Los gastos básicos que registraron mayor alza porcentual mensual
                en {} fueron: {}, {}, {}, {} y {} todo incluido al exterior con
                {} de {:.2f}%, {:.2f}%, {:.2f}%, {:.2f}% y {:.2f}%,
                respectivamente.""".format(fecha, *nombres, tipo, *indices)
    return retocar_plantilla(plantilla)


from sqline import sqlINE
p = sqlINE(2022, 8)
a = p.incidencia_gasto_basico(0)
print(sorted(a)[0:5])
print(incidencias(a , '', False))