# from sqline import sqlINE
from typing import List, Tuple

from utilsjo import mes_anio_by_abreviacion, mes_by_ordinal

class DescriptorIPC:
    def __init__(self, anio: int, mes: int) -> None:
        self.mes = mes
        self.anio = anio
        self.region = dict(zip(
            range(1,9),
            ('I','II','III','IV','V','VI','VII','VIII')))
        self.__notaReg = '''\\footnote{Guatemala se encuentra organizada en 8
            regiones; La región I o Metropolitana está conformada por el
            departamento de Guatemala, la región II o Norte por Alta Verapaz, la
            región III o Nororiental por Chiquimula, e Izabal, la región IV o
            Suroriental por Jutiapa y Jalapa, la región V o Central por
            Chimaltenango, Sacatepéquez y Escuintla, la región VI o
            Suroccidental por Quetzaltenango, Retalhuleu, San Marcos,
            Suchitepéquez, Sololá y Totonicapán, la región VII o Noroccidental
            por Huehuetenango y Quiché y la región VIII por Petén.}'''

    def retocar_plantilla(self, plantilla: str) -> str:
        plantilla = plantilla.replace("\n", " ")
        plantilla = plantilla.split()
        plantilla = " ".join(plantilla)
        return plantilla

    def variacion(self, dato: float, dato_antes: float) -> float:
        """
        Calcula la variación porcentual entre dos valores numéricos.

        Args:
        dato (float): Valor actual.
        dato_antes (float): Valor anterior.

        Returns:
        float: Variación porcentual entre los dos valores.
        """
        return ((dato - dato_antes) / dato_antes) * 100

    def indice_precio_alimentos(self, datos: List[Tuple[str]], precision: int=2) -> str:
        """
        Genera un texto con la información del índice de precios de los alimentos.

        Parameters
        ----------
            datos (List[Tuple[str, float]]): Lista de tuplas que contiene información de fecha y precio.

        Returns
        ----------
            str: Texto con la información del índice de precios de los alimentos.
        """
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(datos[-2][0], mmaa=True)
        indice = datos[-1][1]
        variacion_1 = self.variacion(datos[-1][1], datos[0][1])
        variacion_2 = self.variacion(datos[-1][1], datos[-2][1])
        nota_1 = '''\\footnote{El índice de precios de los alimentos de la FAO
            es una medida de la variación mensual de los precios internacionales
            de una canasta de productos alimenticios. Consiste en el promedio de
            los índices de precios de cinco grupos de productos, ponderado con
            las cuotas medias de exportación de cada uno de los grupos para
            2002-2004.}'''
        nota_2 = '''\\footnote{Organización de las Naciones Unidas para la
            Alimentación y la Agricultura.}'''
        plantilla = f"""En {fecha_1}, el índice de precios de los
            alimentos{nota_1} de la FAO{nota_2} se situó en
            {indice:,.{precision}f} puntos, lo que supone una variación de
            {variacion_1:,.{precision}f}% respecto a {fecha_2}, y del
            {variacion_2:,.2f}% respecto a {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    def petroleo(self, datos: List[Tuple[str, float]], precision: int=2) -> str:
        """
        Función que recibe una lista de tuplas con datos del precio del petróleo
        y devuelve una cadena de texto formateada con la información
        correspondiente.

        Parameters
        ----------
            datos: Lista de tuplas con los datos del precio del petróleo. Cada
            tupla contiene una cadena con la abreviatura del mes y el año
            correspondiente (por ejemplo, "Ene 2022") y un valor float con el
            precio del petróleo en dólares por barril.
        
        Returns
        ----------
            Cadena de texto con la información del precio del petróleo formateada.
        """
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
        plantilla = f"""En {fecha_1}, el precio internacional del petróleo{nota}
            se situó en un promedio de US${PRECIO:,.{precision}f} por barril,
            reflejando una variación de {variacion_1:,.{precision}f}%
            ({signo_1}US${diferencia_1:,.{precision}f}) en comparación con 
            {fecha_2} y de {variacion_2:,.{precision}f}%
            ({signo_2}US${diferencia_2:,.{precision}f}) en relación con
            {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    def cambio_del_quetzal(self, datos: List[Tuple[str, float]], precision: int=2) -> str:
        """
        Retorna un string con información sobre el tipo de cambio del quetzal
        guatemalteco respecto al dólar estadounidense.

        Parameters
        ----------
        datos : list of tuple of str and float
            Una lista de tuplas con información sobre el tipo de cambio. Cada
            tupla contiene una cadena con la abreviación del mes y el año (por
            ejemplo, "Ene 2022") y un valor float con el tipo de cambio en
            quetzales por dólar estadounidense.

        Returns
        -------
        str
            Un string con información sobre el tipo de cambio.
        """
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
        plantilla = f"""En {fecha_1}, el tipo de cambio de referencia{nota} del
            quetzal frente al dólar de los Estados Unidos de América, registró
            un promedio de Q{PRECIO:,.{precision}f} por US$1.00, reflejando una
            variación de {variacion_1:,.{precision}f}% en comparación con
            {fecha_2} y de {variacion_2:,.{precision}f}% en relación con
            {fecha_3}."""
        return self.retocar_plantilla(plantilla)

    def tasa_de_interes(self, datos: List[Tuple[str, float]], precision: int=2) -> str:
        """
        Retorna un string con información sobre la tasa de interés activa en
        moneda nacional.

        Parameters
        ----------
        datos : list of tuple of str and float
            Una lista de tuplas con información sobre la tasa de interés activa.
            Cada tupla contiene una cadena con la abreviación del mes y el año
            (por ejemplo, "Ene 2022") y un valor float con la tasa de interés
            activa en porcentaje.

        Returns
        -------
        str
            Un string con información sobre la tasa de interés activa.
        """
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
            cambio_1 = "un incremento"
        else:
            cambio_1 = "un cambio"
        if diferencia_2 < 0:
            cambio_2 = "una disminución"
            diferencia_2 *= -1
        elif diferencia_2 > 0:
            cambio_2 = "un incremento"
        else:
            cambio_2 = "un cambio"
        nota = """\\footnote{Es el porcentaje que las instituciones bancarias,
                    de acuerdo con las condiciones de mercado y las disposiciones
                    del banco central, cobran por los diferentes tipos de servicios
                    de crédito a los usuarios de los mismos.}"""
        plantilla = f"""En {fecha_1}, el promedio ponderado de la tasa de
            interés activa{nota} en moneda nacional se situó en
            {tasa:,.{precision}f}%, mostrando {cambio_1} de
            {diferencia_1:,.{precision}f} puntos porcentuales en comparación con
            {fecha_2} y {cambio_2} de {diferencia_2:,.{precision}f} puntos
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
    def ipc_usa(self, datos: list[tuple[str]], precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = datos[-1][1] - datos[0][1]
        if diferencia < 0:
            cambio = "desaceleración"
            diferencia *= -1
        elif diferencia > 0:
            cambio = "aceleración"
        else:
            cambio = "cambio"
        nota = """\\footnote{Para mayor información sobre el indice de precios
                    al consumidor de los Estados Unidos, visite
                    \\url{http://www.bls.gov/cpi}.}"""
        plantilla = f"""Durante el período comprendido entre {fecha_2} y
            {fecha_1}, Estados Unidos de América{nota} experimentó un cambio en
            su ritmo inflacionario, de un {indice_2:,.{precision}f}% a
            {indice_1:,.{precision}f}%, lo que representa una {cambio} en
            {diferencia:,.{precision}f} puntos."""
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
    def ipc_mex(self, datos: list[tuple[str]], precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0])
        fecha_2 = mes_anio_by_abreviacion(datos[0][0])
        indice_1 = datos[-1][1]
        indice_2 = datos[0][1]
        diferencia = datos[-1][1] - datos[0][1]
        if diferencia < 0:
            cambio = "desaceleración"
            diferencia *= -1
        elif diferencia > 0:
            cambio = "aceleración"
        else:
            cambio = "cambio"
        nota = """\\footnote{Para mayor información sobre el índice de precios 
            al consumidor en México, visite \\url{http://www.inegi.org.mx}.}"""
        plantilla = f"""Durante el período comprendido entre {fecha_2} y
            {fecha_1}, México{nota} experimentó un cambio en su ritmo
            inflacionario, de un {indice_2:,.{precision}f}% a un
            {indice_1:,.{precision}f}%, lo que representa una {cambio} en
            {diferencia:,.{precision}f} puntos."""
        return self.retocar_plantilla(plantilla)

    def inflacion(self, datos, mes, anio, precision: int=2) -> str:
        inflacion_mes = [(i[2], i[0]) for i in datos[1::]]
        inflacion_mes.sort()
        INFLACION_MIN = inflacion_mes[0]
        INFLACION_MAX = inflacion_mes[-1]
        plantilla = f"""Para el mes de {mes} {anio}, en Centro América,
            República Dominicana y México, {INFLACION_MAX[1]} presentó el mayor
            ritmo inflacionario de {INFLACION_MAX[0]:,.{precision}f}%, mientras
            que {INFLACION_MIN[1]} registró el ritmo inflacionario más bajo con
            un nivel de {INFLACION_MIN[0]:,.{precision}f}%."""
        return self.retocar_plantilla(plantilla)

    def serie_historica_ipc(self, datos, QGba: bool=False, QReg: bool=False, precision: int=2) -> str:
        if QGba:
            gba = f'índice del producto {datos[0].lower()}'
            if (self.anio == 2024):
                datos = datos[1][-1 - self.mes:]
            else:
                datos = datos[1]
        elif QReg:
            gba = 'número índice'
        else:
            gba = 'Índice de Precios al Consumidor (IPC)'
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
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

        if diferencia == 0:
            return self.retocar_plantilla(f"""En los períodos de {fecha_2} y
                {fecha_1} se observó una igualdad en el {gba}.""")
        
        if diferencia > 0:
            cambio = "un aumento"
            diferencia *= -1
        elif diferencia < 0:
            cambio = "una disminución"

        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_3 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_4 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_3 = maximo[0]
        indice_4 = minimo[0]
        plantilla = f"""En los períodos de {fecha_2} y {fecha_1} se observó
            {cambio} en el {gba}, de {indice_2:,.{precision}f} a
            {indice_1:,.{precision}f}, alcanzando el punto más alto en {fecha_3}
            con {indice_3:,.{precision}f} y el más bajo en {fecha_4} con
            {indice_4:,.{precision}f}, esto sugiere que a lo largo del período
            analizado se presentaron fluctuaciones en los niveles de precios por
            diversos factores económicos y estacionales que influyen en la
            dinámica de los precios."""
        return self.retocar_plantilla(plantilla)

    # tipo = intermensual, interanual, acumulada
    def serie_historica_inflacion(self, datos, tipo: str, nivel: str='a nivel nacional', Qmensual: bool=True, precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
        indice_1 = datos[-1][1] # mes actual
        indice_2 = datos[-2][1] # mes anterior
        indice_3 = datos[0][1]
        diferencia_1 = indice_1 - indice_2
        diferencia_2 = indice_1 - indice_3
        
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_4 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_5 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_4 = maximo[0]
        indice_5 = minimo[0]
        
        if diferencia_1 > 0:
            cambio_1 = "una aceleración"
        elif diferencia_1 < 0:
            cambio_1 = "una desaceleración"
            diferencia_1 *= -1
        else:
            cambio_1 = "un cambio"
        if diferencia_2 > 0:
            cambio_2 = "una aceleración"
        elif diferencia_2 < 0:
            cambio_2 = "una desaceleración"
            diferencia_2 *= -1
        else:
            cambio_2 = "un cambio"
        if tipo == "interanual":
            plantilla = f"""En {fecha_1}, el ritmo inflacionario del índice
            {nivel} se situó en {indice_1:,.{precision}f}%. Esta cifra indica
            {cambio_1} en el aumento general de precios, en
            {diferencia_1:,.{precision}f} puntos en comparación con el mes
            anterior ({indice_2:,.{precision}f}%). Además, respecto a la
            variación observada en {fecha_2} ({indice_3:,.{precision}f}%), se
            registró {cambio_2} de {diferencia_2:,.{precision}f} puntos."""
        elif tipo == "acumulada":
            fecha_2 = mes_anio_by_abreviacion(datos[-2][0], mmaa=True)
            fecha_3 = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
            indice_3 = datos[-2][1]
            plantilla = f"""La variación {tipo} en {fecha_1} fue de
                {indice_1:,.{precision}f}%, marcando una disminución respecto al
                valor alcanzado en {fecha_2}, que fue del
                {indice_3:,.{precision}f}%. Dentro del período de {fecha_3} a
                {fecha_1} se observaron fluctuaciones, con el punto más bajo en
                {fecha_5} ({indice_5:,.{precision}f}%) y el más alto en
                {fecha_4} ({indice_4:,.{precision}f}%)."""
        else:
            plantilla = f"""La variación {tipo} del índice {nivel} en {fecha_1},
                se ubicó en {indice_1:,.{precision}f}%. Esta variación
                representa {cambio_1} en el incremento general de precios de
                {diferencia_1:,.{precision}f} puntos porcentuales respecto al
                mes anterior ({indice_2:,.{precision}f}%), y la de {fecha_2} se
                presentó en {indice_3:,.{precision}f}%."""
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
        plantilla = """Los productos que registraron mayor alza porcentual
            mensual en {} fueron: {}, {}, {}, {} y {} todo incluido al exterior
            con {} de {:,.2f}%, {:,.2f}%, {:,.2f}%, {:,.2f}% y {:,.2f}%,
            respectivamente.""".format(fecha, *nombres, tipo, *indices)
        return self.retocar_plantilla(plantilla)

    def poder_adquisitivo(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        perdida = 1 - indice_1
        plantilla = f"""El quetzal experimentó una pérdida de {perdida:,.2f}
            centavos en su poder adquisitivo en comparación con diciembre de
            2023, lo que significa que un quetzal de diciembre de 2023 equivale
            a {indice_1:,.2f} centavos en {fecha_1}."""
        return self.retocar_plantilla(plantilla)

    def serie_fuentes(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""En el período actual, se consultaron un total de
            {indice_1:,} fuentes. Al revisar los registros históricos, se
            identificó un máximo en el mes de {fecha_2}, con {indice_2:,} y un
            mínimo en el mes de {fecha_3}, con {indice_3:,}."""
        return self.retocar_plantilla(plantilla)

    def serie_precios(self, datos) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""Durante el mes de {fecha_1}, se recopilaron un total de
            {indice_1:,} precios. La máxima incidencia se registró en el mes de
            {fecha_2} con {indice_2:,}, en contraste con la cifra mínima
            evidenciada en {fecha_3}, la cual totalizó {indice_3:,}
            observaciones."""
        return self.retocar_plantilla(plantilla)

    def imputacion_precios(self, datos, precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        indice_1 = datos[-1][1]
        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_2 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_3 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_2 = maximo[0]
        indice_3 = minimo[0]
        plantilla = f"""En {fecha_1}, el porcentaje de precios imputados fue de
            {indice_1:.{precision}f}%. El porcentaje más alto se registró en
            {fecha_2}, con {indice_2:.{precision}f}%, y el más bajo en
            {fecha_3}, con {indice_3:.{precision}f}%."""
        return self.retocar_plantilla(plantilla)

    def incidencia_divisiones(self, datos, variacion_mensual: float) -> str:
        datos = sorted(datos, reverse=True)
        maximo1 = datos[0]
        maximo2 = datos[1]
        minimo = datos[-1]
        if variacion_mensual > 0:
            plantilla = f"""De las trece divisiones de gasto que integran el
                IPC, la de {maximo1[1].lower()} ({round(maximo1[0], 2):,.2f}%) y
                {maximo2[1].lower()} ({round(maximo2[0], 2):,.2f}%), registraron
                la mayor incidencia mensual positiva. Por su parte,
                {minimo[1].lower()} es la división de gasto con mayor incidencia
                mensual negativa ({round(minimo[0], 2):,.2f}%)."""
        else:
            plantilla = f"""De las trece divisiones de gasto que integran el
                IPC, la de {minimo[1].lower()} es la división de gasto con menor
                incidencia mensual negativa ({round(minimo[0], 2):,.2f}%). Por
                su parte, {maximo1[1].lower()} ({round(maximo1[0], 2):,.2f}%) y
                {maximo2[1].lower()} ({round(maximo2[0], 2):,.2f}%), registraron
                la mayor incidencia mensual positiva."""
        return self.retocar_plantilla(plantilla)

    def cobertura_fuentes(self, datos) -> str:
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        region = dict(zip(
            range(1,9),
            ('I','II','III','IV','V','VI','VII','VIII')))
        plantilla = f"""En el mes de {mes} {self.anio} la Región{self.__notaReg}
            {region[maximo[0]]} lideró el registro de fuentes consultadas con un
            total de {maximo[1]:,}, en contraste, la Región {region[minimo[0]]}
            presenta la cifra más baja, con {minimo[1]:,}."""
        return self.retocar_plantilla(plantilla)

    def desagregacion_fuentes(self, datos, mes_ordinal, precision: int=2) -> str:
        mes = mes_by_ordinal(mes_ordinal, abreviado=False).lower()
        maximo = datos[0][1]
        fuente_max = datos[0][0].lower()
        minimo = datos[1][1]
        fuente_min = datos[1][0].lower()
        plantilla = f"""En el mes de {mes} {self.anio} las dos tipologías de
            fuentes más consultadas fueron {fuente_max} con un
            {maximo:,.{precision}f}%, y {fuente_min} con un
            {minimo:,.{precision}f}%."""
        return self.retocar_plantilla(plantilla)

    def cobertura_precios(self, datos):
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        plantilla = f"""Como resultado del levantamiento de precios en las
            regiones durante el mes de {mes} {self.anio}, se determinó que la
            Región{self.__notaReg} {self.region[maximo[0]]} presentó la mayor
            cantidad de precios recolectados, alcanzando un total de
            {maximo[1]:,}. Por otro lado, la Región {self.region[minimo[0]]} mostró la cobertura más baja,
            con un total de {minimo[1]:,}."""
        return self.retocar_plantilla(plantilla)

    def ipc_regiones(self, datos, precision: int=2):
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        plantilla = f"""En {mes} de {self.anio}, la Región{self.__notaReg}
            {self.region[maximo[0]]} presenta el punto más alto con un valor de
            {maximo[1]:,.{precision}f}, indicando una mayor presión
            inflacionaria en comparación con otras regiones. En contraste, la
            Región {self.region[minimo[0]]} registra el punto más bajo con un
            valor de {minimo[1]:,.{precision}f}, señalando una menor influencia
            de factores inflacionarios en esta área."""
        return self.retocar_plantilla(plantilla)

    def inflacion_interanual_regiones(self, datos, precision: int=2):
        datos = sorted(datos, key=lambda x: x[1], reverse=True)
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        maximo = datos[0]
        minimo = datos[-1]
        mes = mes_by_ordinal(self.mes, abreviado=False).lower()
        plantilla = f"""En {mes} de {self.anio}, la Región {self.__notaReg}
            {self.region[maximo[0]]} destaca con el ritmo inflacionario más
            alto, alcanzando un valor de {maximo[1]:,.{precision}f}. Por otro
            lado, la Región {self.region[minimo[0]]} presenta el ritmo
            inflacionario más bajo, de {minimo[1]:,.{precision}f}, señalando
            menor influencia de factores inflacionarios en comparación con otras
            regiones."""
        return self.retocar_plantilla(plantilla)

    def incidencias_gba(self, datos, Qpositiva: bool = True):
        if Qpositiva:
            signo = 'positiva'
        else:
            signo = 'negativa'
        textos = []
        for d in datos:
            gba = d[0]
            gba = gba.capitalize()
            indice = d[1]
            tx = f"{gba} ({indice:,.2f}%)"
            textos.append(tx)
        plantilla = """Los cinco productos que presentan la mayor incidencia {}
        mensual son los siguientes: {}, {}, {}, {} y {}.""".format(
            signo,
            *textos)
        return self.retocar_plantilla(plantilla)

    def serie_historica(self, tipo: str) -> str:
        """
        Genera el texto de la serie histórica de IPC, inflación interanual o
        variación mensual.
        Parámetros
        ----------
        tipo: str
            Tipo de serie. Puede ser 'ipc', 'anual' o 'mensual'.
            
        Retorna
        -------
        str
            Texto de la serie histórica.
            
        Excepciones
        -----------
        ValueError
            Si el tipo de serie no es reconocido.  
        """
        if tipo == 'ipc':
            titulo = 'del Índice de precios al consumidor'
        elif tipo == 'anual':
            titulo = 'ritmo inflacionario'
        elif tipo == 'mensual':
            titulo = 'de la variación mensual'
        else:
            raise ValueError('Tipo de serie no reconocido')
        plantilla = """En la siguiente gráfica se presenta la serie histórica {}
            desde el inicio de la base (diciembre de 2023).""".format(titulo)
        return self.retocar_plantilla(plantilla)

    def tabla_serie_historica(self) -> str:
        """
        Genera el texto de la tabla de la serie histórica de IPC, inflación
        interanual o variación mensual.
        Retorna
        -------
        str
            Texto de la tabla de la serie histórica.
        """
        plantilla = """En la siguiente tabla se presenta la serie histórica
                    del ritmo inflacionario, variación mensual e Índice de precios
                    al consumidor desde el inicio de la base (diciembre de 2023)."""
        return self.retocar_plantilla(plantilla)
    
    def serie_historica_mensual_inflacion(self, datos, tipo: str, nivel: str='a nivel nacional', precision: int=2) -> str:
        fecha_1 = mes_anio_by_abreviacion(datos[-1][0], mmaa=True)
        fecha_2 = mes_anio_by_abreviacion(datos[-2][0], mmaa=True)
        indice_1 = datos[-1][1] # mes actual
        indice_2 = datos[-2][1] # mes anterior

        datos_temp = sorted([d[::-1] for d in datos])
        maximo = datos_temp[-1]
        minimo = datos_temp[0]
        fecha_3 = mes_anio_by_abreviacion(maximo[1], mmaa=True)
        fecha_4 = mes_anio_by_abreviacion(minimo[1], mmaa=True)
        indice_3 = maximo[0]
        indice_4 = minimo[0]

        fecha_extra = mes_anio_by_abreviacion(datos[0][0], mmaa=True)
        
        if tipo == "interanual":
            plantilla = f"""En {fecha_1}, se observa un ritmo inflacionario del
                {indice_1:,.{precision}f}%.
                El punto más alto se registró en {fecha_3}, alcanzando un
                porcentaje de {indice_3:,.{precision}f}%.
                En contraste, el punto más bajo se evidenció en {fecha_4}, con
                {indice_4:,.{precision}f}%."""
        else:
            plantilla = f"""En el periodo de {fecha_extra[-4:]} a {fecha_1[-4:]}, la variación
                {tipo} del índice {nivel} muestra que el punto máximo se alcanzó
                en {fecha_3}, con un {indice_3:,.{precision}f}%, mientras que el
                mínimo se registró en {fecha_4}, con {indice_4:,.{precision}f}%.
                En {fecha_1}, la variación fue de {indice_1:,.{precision}f}%.
                Estos resultados resaltan la variabilidad en la dinámica mensual
                de los precios a lo largo de los años."""

        return self.retocar_plantilla(plantilla)
