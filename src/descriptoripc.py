# from sqline import sqlINE
from funcionesjo import mes_anio_by_abreviacion, mes_by_ordinal

class Descriptor:
    def __init__(self, anio: int, mes: int) -> None:
        self.mes = mes
        self.anio = anio

    def retocar_plantilla(self, plantilla: str) -> str:
        plantilla = plantilla.replace("\n", " ")
        plantilla = plantilla.split()
        plantilla = " ".join(plantilla)
        return plantilla

    def variacion(self, dato: float, dato_antes: float) -> float:
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
    def indice_precio_alimentos(self, datos: list[tuple[str]]) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], MMAA=True)
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0], MMAA=True)
        indice = datos[-1][1]
        variacion_1 = self.variacion(datos[-1][1], datos[0][1])
        variacion_2 = self.variacion(datos[-1][1], datos[-2][1])
        nota_1 = '''\\footnote{El índice de precios de los alimentos de la FAO es una medida
                    de la variación mensual de los precios internacionales de
                    una canasta de productos alimenticios. Consiste en el promedio
                    de los índices de precios de cinco grupos de productos básicos,
                    ponderado con las cuotas medias de exportación de cada uno
                    de los grupos para 2002-2004.}'''
        nota_2 = '''\\footnote{Organización de las Naciones Unidas para la
                    Alimentación y la Agricultura.}'''
        plantilla = f"""El índice de precios de los alimentos{nota_1} de la FAO{nota_2} registró en
                    {fecha_1} un índice de {indice:.2f}, lo que representa una
                    variación de {variacion_1:.2f}% respecto a {fecha_2} y de
                    {variacion_2:.2f}% respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)
    # petroleo
    """
    ejemplo de datos
    ('2014-Nov', 75.78947368421052)
    ('2014-Dic', 59.29045454545455)
    ...
    ('2015-Sep', 45.479523809523805)
    ('2015-Oct', 46.22363636363636)
    """
    def petroleo(self, datos: list[tuple[str]]) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0])
        PRECIO = datos[-1][1]
        diferencia_1 = datos[-1][1] - datos[0][1]
        variacion_1 = self.variacion(datos[-1][1], datos[0][1])
        if diferencia_1 > 0:
            signo_1 = ""
        else:
            diferencia_1 = diferencia_1 * -1
            signo_1 = "-"
        diferencia_2 = datos[-1][1] - datos[-2][1]
        variacion_2 = self.variacion(datos[-1][1], datos[-2][1])
        if diferencia_2 > 0:
            signo_2 = ""
        else:
            diferencia_2 = diferencia_2 * -1
            signo_2 = "-"
        nota = """\\footnote{Se refiere al crudo West Texas Intermediate (WTI)
                    producido en Texas y el sur de Oklahoma}"""
        plantilla = f"""El precio internacional del petróleo{nota} registró en {fecha_1}
                    un precio medio de US${PRECIO:.2f} por barril, lo que representa
                    una variación de {variacion_1:.2f}% ({signo_1}US${diferencia_1:.2f})
                    respecto a {fecha_2} y de {variacion_2:.2f}% ({signo_2}US${diferencia_2:.2f})
                    respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    # cambio del quetzal
    """
    ejemplo de datos
    ('2021-Ago', 7.738385161290321)
    ...
    ('2022-Jun', 7.735068333333335)
    ('2022-Jul', 7.739475806451614)
    """
    def cambio_del_quetzal(self, datos: list[tuple[str]]) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0])
        PRECIO = datos[-1][1]
        variacion_1 = self.variacion(datos[-1][1], datos[0][1])
        variacion_2 = self.variacion(datos[-1][1], datos[-2][1])
        nota = """\\footnote{El tipo de cambio de referencia lo calcula el Banco
                    de Guatemala con la información que las instituciones que
                    constituyen el Mercado Institucional de Divisas le proporcionan,
                    relativa al monto de divisas compradas y al monto de divisas
                    vendidas y sus respectivas equivalencias en moneda nacional.}"""
        plantilla = f"""El tipo de cambio de referencia{nota} del quetzal respecto al dólar
                    de los Estados Unidos de América, registró en {fecha_1} un precio
                    medio de Q{PRECIO:.2f} por US$1.00, lo que representa una variación
                    de {variacion_1:.2f}% respecto a {fecha_2} y de {variacion_2:.2f}%
                    respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    # tasa de interes
    """
    ('2021-Ago', 12.139999999999999)
    ('2021-Sep', 12.16)
    ...
    ('2022-Abr', 11.93)
    ('2022-May', 11.940000000000001)
    ('2022-Jun', 11.98)
    """
    def tasa_de_interes(self, datos: list[tuple[str]]) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0])
        tasa = datos[-1][1]
        diferencia_1 = datos[-1][1] - datos[0][1]
        diferencia_2 = datos[-1][1] - datos[-2][1]
        if diferencia_1 < 0:
            cambio_1 = "una disminución"
            diferencia_1 *= -1
        elif diferencia_1 > 0:
            cambio_1 = "un aumento"
        else:
            cambio_1 = "un cambio"
        if diferencia_2 < 0:
            cambio_2 = "una disminución"
            diferencia_2 *= -1
        elif diferencia_2 > 0:
            cambio_2 = "un aumento"
        else:
            cambio_2 = "un cambio"
        nota = """\\footnote{Es el porcentaje que las instituciones bancarias,
                    de acuerdo con las condiciones de mercado y las disposiciones
                    del banco central, cobran por los diferentes tipos de servicios
                    de crédito a los usuarios de los mismos.}"""
        plantilla = f"""El promedio ponderado preliminar de la tasa de interés activa{nota}
                    en moneda nacional se ubicó en {fecha_1} en {tasa:.2f}%, lo que
                    representa {cambio_1} de {diferencia_1:.2f} puntos porcentuales
                    respecto a {fecha_2} y {cambio_2} de {diferencia_2:.2f} puntos
                    porcentuales respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    # IPC USA
    """
    ejemplo de datos
    ('2021-Ago', 5.205331689652515)
    ('2021-Sep', 5.389907375379521)
    ...
    ('2022-May', 8.516412942713858)
    ('2022-Jun', 8.995220608588127)
    """
    def ipc_usa(self, datos: list[tuple[str]]) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = datos[-1][1] - datos[0][1]
        if diferencia < 0:
            cambio = "se desaceleró"
            diferencia *= -1
        elif diferencia > 0:
            cambio = "se aceleró"
        else:
            cambio = "cambio"
        nota = """\\footnote{Para mayor información sobre el indice de precios
                    al consumidor de los Estados Unidos, visite
                    \\url{http://www.bls.gov/cpi}.}"""
        plantilla = f"""El Índice de Precios al Consumidor en los Estados Unidos de
                    América{nota} registró una variación interanual al mes de {fecha_1} de
                    {indice_1:.2f}%. En {fecha_2} la variación interanual se ubicó en
                    {indice_2:.2f}%, por lo que este indicador {cambio} {diferencia:.2f}
                    puntos porcentuales en el último año."""
        return self.retocar_plantilla(plantilla)

    # IPC MEX
    """
    ejemplo de datos
    ('2021-Ago', 5.205331689652515)
    ('2021-Sep', 5.389907375379521)
    ...
    ('2022-May', 8.516412942713858)
    ('2022-Jun', 8.995220608588127)
    """
    def ipc_mex(self, datos: list[tuple[str]]) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = datos[-1][1] - datos[0][1]
        if diferencia < 0:
            cambio = "se desaceleró"
            diferencia *= -1
        elif diferencia > 0:
            cambio = "se aceleró"
        else:
            cambio = "cambio"
        nota = """\\footnote{Para mayor información sobre el índice de precios
                    al consumidor en México, visite \\url{http://www.inegi.org.mx}.}"""
        plantilla = f"""El Índice de Precios al Consumidor en México{nota} de registró una
                    variación interanual al mes de {fecha_1} de {indice_1:.2f}%. En
                    {fecha_2} la variación interanual se ubicó en {indice_2:.2f}%,
                    por lo que este indicador {cambio} {diferencia:.2f} puntos
                    porcentuales en el último año."""
        return self.retocar_plantilla(plantilla)

    def inflacion(self, datos, mes, anio) -> str:
        inflacion_mes = [(i[1], i[0]) for i in datos[1::]]
        inflacion_mes.sort()
        INFLACION_MIN = inflacion_mes[0]
        INFLACION_MAX = inflacion_mes[-1]
        plantilla = f"""Para el mes de {mes} {anio}, en Centro América, República
                    Dominicana y México, {INFLACION_MAX[1]} presentó
                    la mayor tasa de inflación interanual de {INFLACION_MAX[0]:.2f}%,
                    mientras que {INFLACION_MIN[1]} registró la tasa más
                    baja con un nivel de {INFLACION_MIN[0]:.2f}%."""
        return self.retocar_plantilla(plantilla)

    def serie_historica_ipc(self, datos, QGba: bool=False) -> str:
        if QGba:
            gba = f'gasto basico {datos[0].lower()}'
            datos = datos[1]
        else:
            gba = 'Índice de Precios al Consumidor'
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], MMAA=True)
        if datos[-1][0].split('-')[0] == datos[0][0].split('-')[0]:
            Qmismo_anio = False
        else:
            Qmismo_anio = True
        if Qmismo_anio:
            plantilla_aux = f'{fecha_2}'
        else:
            plantilla_aux = 'el mismo mes del año anterior'

        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = indice_1 - indice_2
        if diferencia > 0:
            cambio = "mayor"
            diferencia *= -1
        elif diferencia < 0:
            cambio = "menor"
        else:
            cambio = "igual"
        plantilla = f"""El {gba} a {fecha_1} se ubicó en
                    {indice_1:.2f}, {cambio} a lo observado en {plantilla_aux}
                    ({indice_2:.2f})."""
        return self.retocar_plantilla(plantilla)

    # tipo = intermensual, interanual, acumulada
    def serie_historica_inflacion(self, datos, tipo: str, nivel: str='nacional') -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], MMAA=True)
        indice_1 = datos[-1][1] # mes actual
        indice_2 = datos[-2][1] # mes anterior
        indice_3 = datos[0][1]
        diferencia_1 = indice_1 - indice_2
        diferencia_2 = indice_1 - indice_3
        if diferencia_1 > 0:
            cambio_1 = "un aumento"
        elif diferencia_1 < 0:
            cambio_1 = "una disminución"
            diferencia_1 *= -1
        else:
            cambio_1 = "un cambio"
        if diferencia_2 > 0:
            cambio_2 = "un aumento"
        elif diferencia_2 < 0:
            cambio_2 = "una disminución"
            diferencia_2 *= -1
        else:
            cambio_2 = "un cambio"
        plantilla = f"""La variación {tipo} del IPC a nivel {nivel} en {fecha_1},
                    se ubicó en {indice_1:.2f}%. Esta variación representa {cambio_1}
                    en el nivel de precios de {diferencia_1:.2f} puntos porcentuales
                    respecto al mes anterior ({indice_2:.2f}%), y con respecto a la
                    variación alcanzada en {fecha_2} ({indice_3:.2f}%) {cambio_2} de
                    {diferencia_2:.2f} puntos."""
        return self.retocar_plantilla(plantilla)

    def incidencia_divisiones(self, datos, fecha) -> str:
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
        return self.retocar_plantilla(plantilla)

    def incidencias(self, datos, fecha: str, Qpositivas: bool=True) -> str:
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
        return self.retocar_plantilla(plantilla)

    def poder_adquisitivo(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], MMAA=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], MMAA=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""El poder adquisitivo del quetzal a {fecha_1} es de {indice_1:.2f}.
                    El mayor valor adquisitivo se encuentra en el mes de {fecha_2}
                    con un valor de {indice_2:.2f} y el menor se encuentra en el mes
                    de {fecha_3} con un valor de {indice_3:.2f}."""
        return self.retocar_plantilla(plantilla)

    def serie_fuentes(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], MMAA=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], MMAA=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""La cantidad de fuentes consultadas en {fecha_1} es de {indice_1}.
                    La mayor cantidad de fuentes consultadas fue en el mes de {fecha_2}
                    con una cantidad de {indice_2} y la menor se encuentra en el mes
                    de {fecha_3} con una cantidad de {indice_3}."""
        return self.retocar_plantilla(plantilla)

    def serie_precios(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], MMAA=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], MMAA=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""La cantidad de precios diligenciados en {fecha_1} es de {indice_1}.
                    La mayor cantidad de precios diligenciados fue en el mes de {fecha_2}
                    con una cantidad de {indice_2} y la menor se encuentra en el mes
                    de {fecha_3} con una cantidad de {indice_3}."""
        return self.retocar_plantilla(plantilla)

    def imputacion_precios(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], MMAA=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], MMAA=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], MMAA=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""La cantidad de precios imputados en {fecha_1} es de {indice_1}.
                    La mayor cantidad de imputaciones fue en el mes de {fecha_2}
                    con una cantidad de {indice_2} y la menor se encuentra en el mes
                    de {fecha_3} con una cantidad de {indice_3}."""
        return self.retocar_plantilla(plantilla)

    def incidencia_divisiones(self, datos) -> str:
        datos = sorted(datos, reverse=True)
        maximo1 = datos[0]
        maximo2 = datos[1]
        minimo = datos[-1]
        plantilla = f"""De las doce divisiones de gasto que integran
                    el IPC, la de {maximo1[1].lower()} ({round(maximo1[0], 2):.2f}%) y
                    {maximo2[1].lower()} ({round(maximo2[0], 2):.2f}%), registraron la mayor
                    incidencia mensual. Por su parte, {minimo[1].lower()} es la división
                    de gasto con menor incidencia mensual ({round(minimo[0], 2):.2f}%)."""
        return self.retocar_plantilla(plantilla)

    def cobertura_fuentes(self, datos) -> str:
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        nota = '''\\footnote{Guatemala se encuentra organizada en 8 regiones; La región I
                o Metropolitana está conformada por el departamento de Guatemala,
                la región II o Norte por Alta Verapaz y Baja Verapaz, la región III
                o Nororiental por Chiquimula, El Progreso, Izabal y Zacapa, la región
                IV o Suroriental por Jutiapa, Jalapa y Santa Rosa, la región V o Central
                por Chimaltenango, Sacatepéquez y Escuintla, la región VI o Suroccidental 
                por Quetzaltenango, Retalhuleu, San Marcos, Suchitepéquez, Sololá y Totonicapán,
                la región VII o Noroccidental por Huehuetenango y Quiché y la región VIII por Petén.}'''
        region = dict(zip(range(1,9), ('I','II','III','VI','V','VI','VII','VIII')))
        plantilla = f"""En el mes de {mes} {self.anio} la región{nota} {region[maximo[0]]}
                    fue donde mas fuentes fueron consultadas con un total de
                    {maximo[1]} y la región {region[minimo[0]]} fue donde menos fuentes
                    fueron consultadas con un total de {minimo[1]}."""
        return self.retocar_plantilla(plantilla)

    def desagregacion_fuentes(self, datos, mes_ordinal) -> str:
        mes = mes_by_ordinal(mes_ordinal, abreviado=False).lower()
        maximo = datos[0][1]
        fuente_max = datos[0][0].lower()
        minimo = datos[-1][1]
        fuente_min = datos[-1][0].lower()
        plantilla = f"""En el mes de {mes} el tipo de fuente mas consultado fue
                    {fuente_max} ({maximo:.2f}%), y el tipo menos consultado fue
                    {fuente_min} ({minimo:.2f}%)."""
        return self.retocar_plantilla(plantilla)

    def cobertura_precios(self, datos):
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        region = dict(zip(range(1,9), ('I','II','III','VI','V','VI','VII','VIII')))
        plantilla = f"""En el mes de {mes} {self.anio} la region {region[maximo[0]]}
                    fue donde mas precios fueron diligenciados con un total de
                    {maximo[1]} y la region {region[minimo[0]]} fue donde menos precios
                    fueron diligenciados con un total de {minimo[1]}."""
        return self.retocar_plantilla(plantilla)