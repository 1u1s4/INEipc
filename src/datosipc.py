import xml.etree.ElementTree as ET
import requests
import json
import xlrd
from fredapi import Fred
import funcionesjo as Jo
from descriptoripc import Descriptor
from bs4 import BeautifulSoup
from sqline import sqlINE
import pandas as pd
import numpy as np
import calendar
from typing import List, Tuple

class datosIPC:
    def __init__(self, anio: int, mes: int, QdbAux: bool = False, dbBackup: bool = False) -> None:
        """
        Constructor de la clase datosIPC, que permite manejar los datos del IPC y descripciones.

        Parameters
        ----------
        anio : int
            Año en el que se desea obtener los datos del IPC.
        mes : int
            Mes en el que se desea obtener los datos del IPC.
        QdbAux : bool, optional
            Indica si se utiliza una base de datos auxiliar (por defecto, False).
        dbBackup : bool, optional
            Indica si se utiliza una copia de seguridad de la base de datos (por defecto, False).
        """

        self._FORMATO = "%Y-%m-%d"
        self.mes = mes
        self.anio = anio
        self.SQL = sqlINE(anio, mes, QdbAux, dbBackup)
        self.Descriptor = Descriptor(anio, mes) 

    def indice_precio_alimentos(self) -> Tuple[List[Tuple[str, float]], str]:
        """
        Obtiene el índice de precios de los alimentos de los últimos 13 meses desde la FAO y su descriptor.

        Returns
        -------
        tuple
            - Una lista de tuplas que contiene el índice de precios de los alimentos de los últimos 13 meses
              en el formato (mes-año, índice).
            - Descriptor del índice de precios de los alimentos basado en el último mes.
        """
        # web scraping para encontrar el link actualizado
        URL = "https://www.fao.org/worldfoodsituation/foodpricesindex/en/"
        HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        r = requests.get(url=URL, headers=HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            url = link['href']
            if "Food_price_indices_data_" in url and "xls" in url: 
                url = f"https://www.fao.org{url}"
                break
        # descargar datos
        DATA_URL = url
        with open('FFPI.xls', 'wb') as f:
            r = requests.get(DATA_URL, allow_redirects=True)
            f.write(r.content)
            f.close()
        df = pd.read_excel('FFPI.xls', header=2, usecols='A:B')
        df['Date'] = df['Date'].astype('str')
        data = []
        for i in range(13):
            dato_i = df.iloc[i-13]
            fecha = dato_i['Date'].split('-')
            indice = dato_i['Food Price Index']
            fecha = Jo.mes_by_ordinal(fecha[1]) + '-' + fecha[0]
            data.append((fecha, indice))
        return(data, self.Descriptor.indice_precio_alimentos(data))

    def __petroleo_series_mean(self, anio: int, mes: int) -> float:
        """
        Calcula el promedio del precio del petróleo en un mes específico de un año dado.

        Parameters
        ----------
        anio : int
            Año en el que se desea calcular el promedio del precio del petróleo.
        mes : int
            Mes en el que se desea calcular el promedio del precio del petróleo.

        Returns
        -------
        float
            Promedio del precio del petróleo en el mes especificado del año dado.
        """
        API_KEY ='734b605521e7734edc09f38e977fe238'
        SERIES_ID = 'DCOILWTICO'
        fred = Fred(api_key=API_KEY)
        FECHA_INICIAL = f"{anio}-{mes:02}-01"
        ultimo_dia = calendar.monthrange(anio, mes)[1]
        FECHA_FINAL = f"{anio}-{mes:02}-{ultimo_dia}"
        # carga de datos
        data = fred.get_series(
            series_id=SERIES_ID,
            observation_start=FECHA_INICIAL,
            observation_end=FECHA_FINAL
        )
        data = data.dropna()
        return data.mean()

    def petroleo(self) -> Tuple[List[Tuple[str, float]], str]:
        """
        Calcula la media de la serie de petróleo en un rango de fechas y devuelve
        una tupla con los datos y el descriptor de petróleo.

        Returns:
            tuple: Una tupla que contiene una lista de tuplas (fecha, media) y
                el descriptor de petróleo.
        """
        data = []
        if self.mes == 12:
            for mes in range(1, 13):
                fecha = f'{self.anio}-{Jo.mes_by_ordinal(mes)}'
                media = self.__petroleo_series_mean(self.anio, mes)
                data.append((fecha, media))
        else:
            for mes in range(self.mes, 13):
                fecha = f'{self.anio - 1}-{Jo.mes_by_ordinal(mes)}'
                media = self.__petroleo_series_mean(self.anio - 1, mes)
                data.append((fecha, media))
            for mes in range(1, self.mes + 1):
                fecha = f'{self.anio}-{Jo.mes_by_ordinal(mes)}'
                media = self.__petroleo_series_mean(self.anio, mes)
                data.append((fecha, media))
            
        return (data, self.Descriptor.petroleo(data))

    def cambio_quetzal(self) -> Tuple[List[Tuple[str, float]], str]:
        """
        Retorna una tupla con una lista de tuplas y un string. La lista de tuplas
        contiene información sobre el cambio del quetzal respecto al dólar de los
        Estados Unidos de América. El string contiene información sobre la tasa
        de interés activa en moneda nacional.

        Returns
        -------
        tuple of list of tuple of str and float and str
            Una tupla que contiene una lista de tuplas con información sobre el
            cambio del quetzal respecto al dólar de los Estados Unidos de América
            y un string con información sobre la tasa de interés activa en moneda
            nacional.
        """
        FORMATO = "%d/%m/%Y"
        FECHA_FINAL = f"28/{self.mes}/{self.anio}"
        FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL, formato=FORMATO, inicio_de_mes=True)
        # SOAP request URL
        URL = "http://www.banguat.gob.gt/variables/ws/TipoCambio.asmx"
        PAYLOAD = """<?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
        <soap12:Body>
            <TipoCambioRango xmlns="http://www.banguat.gob.gt/variables/ws/">
            <fechainit>{}</fechainit>
            <fechafin>{}</fechafin>
            </TipoCambioRango>
        </soap12:Body>
        </soap12:Envelope>""".format(FECHA_INICIAL, FECHA_FINAL)
        # headers
        HEADERS = {
            'Content-Type': 'text/xml; charset=utf-8'
        }
        # POST request
        response = requests.request("POST", URL, headers=HEADERS, data=PAYLOAD)
        # parsear XML
        with open("cambio.xml", "w") as f:
            f.write(response.text)
            f.close()
        tree = ET.parse("cambio.xml")
        root = tree.getroot()
        # analisis de los datos
        fecha_i = FECHA_INICIAL
        mes_actual = "-".join((fecha_i.split("/")[2], Jo.mes_by_ordinal(int(fecha_i.split("/")[1]))))
        datos_mes = []
        data_mean = []
        i = 0
        for cambio in root[0][0][0][0]:
            i += 1
            fecha_i = cambio[1].text
            mes_actual_i = "-".join((fecha_i.split("/")[2], Jo.mes_by_ordinal(fecha_i.split("/")[1])))
            # la ultima comparacion es para calcular el promedio del ultimo mes
            if mes_actual_i != mes_actual or i == len(root[0][0][0][0]):
                data_mean.append((mes_actual, sum(datos_mes)/len(datos_mes)))
                datos_mes = []
                mes_actual = mes_actual_i
            try:
                precio = float(cambio[2].text)
                datos_mes.append(precio)
            except:
                None
        return (Jo.invertir_orden(data_mean), self.Descriptor.cambio_del_quetzal(data_mean))

    def tasa_interes(self, fecha_final: str, fecha_inicial: str) -> Tuple[List[Tuple[str, float]], str]:
        """
        Calcula la tasa de interés entre dos fechas y devuelve una lista de tuplas con las tasas de interés y un descriptor.
        
        Parameters
        ----------
        fecha_final : str
            Fecha final en formato 'YYYY-MM'. Si no se proporciona, se utiliza la fecha actual.
        fecha_inicial : str
            Fecha inicial en formato 'YYYY-MM'. Si no se proporciona, se utiliza un año antes de la fecha final.
            
        Returns
        -------
        tuple
            Una tupla que contiene una lista de tuplas con las tasas de interés y un descriptor.
        """
        FORMATO = "%Y-%m"
        if len(fecha_final) == 0:
            FECHA_FINAL = Jo.hoy(FORMATO)
        else:
            FECHA_FINAL = fecha_final
        if len(fecha_inicial) == 0:
            FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL, formato=FORMATO)
        else:
            FECHA_INICIAL = fecha_inicial
        # descarga de datos
        DATA_URL = "https://banguat.gob.gt/sites/default/files/banguat/imm/imm04.xls"
        with open('tasa_interes.xls', 'wb') as f:
            r = requests.get(DATA_URL, allow_redirects=True)
            f.write(r.content)
            f.close()
        # 1996  - col 2
        # enero - fil 5 
        book = xlrd.open_workbook("tasa_interes.xls")
        sh = book.sheet_by_index(0)
        data = []
        COL = int(FECHA_INICIAL.split("-")[0]) - 1994
        for i in range(int(FECHA_INICIAL.split("-")[1]) + 3, 12 + 5):
            marca_temp = FECHA_INICIAL.split("-")[0] + "-" + Jo.mes_by_ordinal(str(i - 4).rjust(2, "0"))
            interes = sh.cell_value(rowx=i, colx=COL)
            if interes != "":
                data.append((marca_temp, 100*interes))
        COL = int(FECHA_FINAL.split("-")[0]) - 1994
        for i in range(5, int(FECHA_FINAL.split("-")[1]) + 4 + 1):
            marca_temp = FECHA_FINAL.split("-")[0] + "-" + Jo.mes_by_ordinal(str(i - 4).rjust(2, "0"))
            interes = sh.cell_value(rowx=i, colx=COL)
            if interes != "":
                data.append((marca_temp, 100*interes))
        return (Jo.invertir_orden(data), self.Descriptor.tasa_de_interes(data))

    def ipc_usa(self) -> Tuple[List[Tuple[str, float]], str]:
        """
        Calcula la variación interanual del IPC de Estados Unidos y retorna una lista de tuplas con la variación
        por mes y una descripción.

        Returns
        -------
        tuple:
            - List[Tuple[str, float]]: Lista de tuplas que contiene la fecha (año-mes) y la variación interanual
            del IPC de Estados Unidos en porcentaje.
            - str: Descripción de la variación interanual del IPC de Estados Unidos.
        """
        FECHA_FINAL = Jo.month_before(f"{self.anio}-{self.mes:0>2}-01")
        FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL)
        FECHA_INICIAL_INICIAL = Jo.year_ago(fecha=FECHA_INICIAL, inicio_de_anio=True)

        API_KEY = '734b605521e7734edc09f38e977fe238'
        fred = Fred(api_key=API_KEY)
        data = fred.get_series('CPIAUCNS', observation_start=FECHA_INICIAL_INICIAL, observation_end=FECHA_FINAL)
        fecha_i = FECHA_INICIAL
        datos_variacion_interanual = []
        for i in range(13):
            try:
                precio = data.dropna().loc[fecha_i]
                precio_anterior = data.dropna().loc[Jo.year_ago(fecha_i)]
                mes_actual_i = "-".join((fecha_i.split("-")[0], Jo.mes_by_ordinal(fecha_i.split("-")[1])))
                variacion = ((precio / precio_anterior) - 1) * 100
                datos_variacion_interanual.append((mes_actual_i, variacion))
                fecha_i = Jo.month_after(fecha_i)
            except:
                pass
        return (Jo.invertir_orden(datos_variacion_interanual), self.Descriptor.ipc_usa(datos_variacion_interanual))

    def ipc_mex(self) -> Tuple[List[Tuple[str, float]],str]:
        """
        Obtiene el índice de precios al consumidor (IPC) de México y calcula la tasa de variación interanual.

        Returns
        -------
        tuple
            Un tuple con dos elementos:
            1. Una lista de tuplas que contiene la fecha (str) y la tasa de variación interanual (float) del IPC.
            2. Un tuple que contiene la fecha (str) y el último valor del IPC (float).
        """
        FECHA_FINAL = Jo.month_before(f"{self.anio}-{self.mes}-01")
        FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL, formato="%Y-%m-%d")
        API_KEY = "515963d6-1153-e348-8394-a81acec0d6da"
        #Llamado al API
        URL = f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/628222/es/0700/false/BIE/2.0/{API_KEY}?type=json'
        response= requests.get(URL)
        data = {}
        if response.status_code == 200:
            content = json.loads(response.content)
            series = content["Series"]
            for i in series[0]["OBSERVATIONS"]:
                marca_temporal = "-".join(i["TIME_PERIOD"].split("/")[0:2])
                data[marca_temporal] = float(i["OBS_VALUE"])
        # ya una vez cargada la informacion se hace la tasa de variacion
        fecha_i = FECHA_INICIAL
        datos_variacion_interanual = []
        for i in range(13):
            try:
                precio = data[Jo.date_mini(fecha_i)]
                precio_anterior = data[Jo.date_mini(Jo.year_ago(fecha_i))]
                mes_actual_i = "-".join((fecha_i.split("-")[0], Jo.mes_by_ordinal(fecha_i.split("-")[1])))
                variacion = ((precio / precio_anterior) - 1) * 100
                datos_variacion_interanual.append((mes_actual_i, variacion))
                fecha_i = Jo.month_after(fecha_i)
            except:
                pass
        return(Jo.invertir_orden(datos_variacion_interanual), self.Descriptor.ipc_mex(datos_variacion_interanual))

    def inflacion_CA_RD_MEX(self) -> Tuple[List[Tuple[str, float, float]], str]:
        """
        Calcula la inflación interanual de varios países de Centroamérica, República Dominicana y México.
        
        Args:
        - self: objeto que representa la clase actual.
        
        Returns:
        - data: lista de tuplas con información de la inflación interanual de cada país. Cada tupla tiene la siguiente información:
            - str: nombre del país.
            - float: inflación interanual del año anterior.
            - float: inflación interanual del año actual.
        - Descriptor.inflacion(data, mes_actual.lower(), self.anio): llamada a un método de la clase Descriptor que devuelve una cadena
        que describe la inflación en los países seleccionados para el mes y año proporcionados.
        """
        paises: Tuple[str, ...] = ("Guatemala", "El Salvador", "Honduras", "Nicaragua", "Costa Rica", "Republica Dominicana", "Panamá", "México")
        mes: str = Jo.mes_by_ordinal(self.mes)
        data: List[Tuple[str, str, str]] = [("Pais", f"{mes}-{self.anio - 1}", f"{mes}-{self.anio}")]
        mes_actual: str = Jo.mes_by_ordinal(self.mes, abreviado=False)
        for pais in paises:
            df = pd.read_excel('IPC CA RD Y MEX.xlsx', sheet_name=pais)
            # inflacion interanual del mes actual
            mes_ = df["mes"] == mes_actual
            anio_ = df["anio"] == self.anio
            indice_actual = df[mes_ & anio_]["indice"].iloc[0]
            mes_ = df["mes"] == mes_actual
            anio_ = df["anio"] == (self.anio - 1)
            indice_anterior = df[mes_ & anio_]["indice"].iloc[0]
            inflacion_actual = (indice_actual/indice_anterior - 1) * 100 
            # inflacion interanual del anio anterior
            mes_ = df["mes"] == mes_actual
            anio_ = df["anio"] == (self.anio - 1)
            indice_actual = df[mes_ & anio_]["indice"].iloc[0]
            mes_ = df["mes"] == mes_actual
            anio_ = df["anio"] == (self.anio - 2)
            indice_anterior = df[mes_ & anio_]["indice"].iloc[0]
            inflacion_anterior = (indice_actual/indice_anterior - 1) * 100 
            data.append((pais, inflacion_anterior, inflacion_actual))
        return (data, self.Descriptor.inflacion(data, mes_actual.lower(), self.anio))

# para el capitulo 3
    def serie_IPC(self, RegCod: int, QGba: bool = False) -> Tuple[List, str]:
        """
        Devuelve una serie histórica de los índices de precios al consumidor para una región específica.
        
        Parameters
        ----------
        - RegCod (int): código de la región para la que se desea obtener la serie histórica.
        - QGba (bool): indica si se desea obtener la serie de datos ajustada por estacionalidad. Por defecto es False.
        
        Returns:
        - datos: lista de datos que representan la serie histórica de los índices de precios al consumidor.
        - descripcion: cadena que describe la serie histórica obtenida.
        """
        datos = self.SQL.serie_historica_ipc_pdr_adq(RegCod)
        descripcion = self.Descriptor.serie_historica_ipc(datos, QGba)
        return(datos, descripcion)
    
    def serie_inflacion(self, RegCod: int, tipo: str, nivel: str='nacional') -> Tuple[List, str]:
        """
        Devuelve una serie histórica de la inflación para una región específica y tipo de índice.
        
        Parameters
        ----------
        - RegCod (int): código de la región para la que se desea obtener la serie histórica.
        - tipo (str): tipo de índice para el que se desea obtener la serie histórica.
        - nivel (str): nivel de desagregación para el que se desea obtener la serie histórica. Por defecto es 'nacional'.
        
        Returns:
        ----------
        - datos: lista de datos que representan la serie histórica de la inflación.
        - descripcion: cadena que describe la serie histórica obtenida.
        """
        datos = self.SQL.serie_historica_inflacion(RegCod, tipo)
        descripcion = self.Descriptor.serie_historica_inflacion(datos, tipo, nivel)
        return(datos, descripcion)

    def serie_poder_adquisitivo(self, RegCod: int) -> Tuple[List, str]:
        """
        Calcula la serie histórica del poder adquisitivo en base al IPC (Índice
        de Precios al Consumidor) para una región dada.

        Parameters
        ----------
        RegCod : int
            Código de la región para la cual se desea calcular el poder adquisitivo.

        Returns
        -------
        datos : pd.DataFrame
            Dataframe que contiene la serie histórica del poder adquisitivo en
            base al IPC para la región especificada.
        descripcion : str
            Descripción textual del poder adquisitivo en base a los datos obtenidos.
        """
        datos = self.SQL.serie_historica_ipc_pdr_adq(RegCod, True)
        descripcion = self.Descriptor.poder_adquisitivo(datos)
        return(datos, descripcion)

    def series_Gba(self, RegCod: int) -> List[Tuple[str, List, str]]:
        """
        Obtiene las series históricas de IPC (Índice de Precios al Consumidor) para diferentes subregiones de una región dada.

        Parameters
        ----------
        RegCod : int
            Código de la región para la cual se desea obtener las series históricas de IPC de sus subregiones.

        Returns
        -------
        salidas : List[Tuple[str, pd.DataFrame, str]]
            Lista de tuplas que contienen el nombre de la subregión (NomGba), el dataframe con la serie histórica de IPC (datos_i),
            y una descripción textual de la serie histórica (descripcion).
        """
        salidas = [] # (NomGba, datos, descripcion)
        datos = self.SQL.series_historicas_Gbas(RegCod)
        for dt in datos:
            NomGba = dt[0] 
            datos_i = dt[1]
            descripcion = self.Descriptor.serie_historica_ipc(dt, True)
            salidas.append((NomGba, datos_i, descripcion))
        return salidas
    
    def serie_fuentes(self) -> Tuple[List, str]:
        """
        Obtiene la serie histórica de precios basada en diferentes fuentes.

        Returns
        -------
        datos : pd.DataFrame
            Dataframe que contiene la serie histórica de precios basada en diferentes fuentes.
        descripcion : str
            Descripción textual de la serie histórica de precios basada en las fuentes de datos obtenidas.
        """
        datos = self.SQL.serie_fuentes_precios()
        descripcion = self.Descriptor.serie_fuentes(datos)
        return(datos, descripcion)

    def serie_precios(self) -> Tuple[List, str]:
        """
        Obtiene la serie histórica de precios sin considerar las diferentes fuentes.

        Returns
        -------
        datos : pd.DataFrame
            Dataframe que contiene la serie histórica de precios sin considerar las diferentes fuentes.
        descripcion : str
            Descripción textual de la serie histórica de precios sin considerar las fuentes de datos.
        """
        datos = self.SQL.serie_fuentes_precios(False)
        descripcion = self.Descriptor.serie_precios(datos)
        return(datos, descripcion)

    def serie_imputacion(self) -> Tuple[List[Tuple[str, float]], str]:
        """
        Obtiene la serie de imputación de precios basada en un archivo de Excel con datos de periodos de espera por década.

        Returns
        -------
        serie : List[Tuple[str, float]]
            Lista de tuplas que contienen la fecha (en formato 'mes-año') y el porcentaje de imputación de precios.
        descripcion : str
            Descripción textual de la serie de imputación de precios.
        """
        serie = []
        df = pd.read_excel('BASE DE DATOS PERIODOS DE ESPERA POR DECADA.xlsx', sheet_name=1).fillna(0)
        df['Prec_PE'] = pd.to_numeric(df['Prec_PE'], errors='coerce')
        df['Prec_Recup'] = pd.to_numeric(df['Prec_Recup'], errors='coerce')
        df['Prec_Pre'] = pd.to_numeric(df['Prec_Pre'], errors='coerce')
        df = df.replace(np.nan, 0, regex=True)
        if self.mes == 12:
            for i in range(1, 13):
                mes_abr = Jo.mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = df['Mes'] == i
                anio_ = df['Año'] == self.anio
                df_i = df[mes_ & anio_].reset_index()
                precios_espera = df_i['Prec_PE'].sum()
                precios_recuperados = df_i['Prec_Recup'].sum()
                precios_prediligenciados = df_i['Prec_Pre'].sum()
                d = (precios_espera - precios_recuperados) / precios_prediligenciados * 100
                if d == np.nan:
                    d = 0
                serie.append((fecha, d))
        else:
            for i in range(self.mes, 13):
                mes_abr = Jo.mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio - 1}'
                mes_ = df['Mes'] == i
                anio_ = df['Año'] == self.anio - 1
                df_i = df[mes_ & anio_].reset_index()
                precios_espera = df_i['Prec_PE'].sum()
                precios_recuperados = df_i['Prec_Recup'].sum()
                precios_prediligenciados = df_i['Prec_Pre'].sum()
                d = (precios_espera - precios_recuperados) / precios_prediligenciados * 100
                if d == np.nan:
                    d = 0
                serie.append((fecha, d))
            for i in range(1, self.mes + 1):
                mes_abr = Jo.mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = df['Mes'] == i
                anio_ = df['Año'] == self.anio
                df_i = df[mes_ & anio_].reset_index()
                precios_espera = df_i['Prec_PE'].sum()
                precios_recuperados = df_i['Prec_Recup'].sum()
                precios_prediligenciados = df_i['Prec_Pre'].sum()
                d = (precios_espera - precios_recuperados) / precios_prediligenciados * 100
                if d == np.nan:
                    d = 0
                serie.append((fecha, d))
        descripcion = self.Descriptor.imputacion_precios(serie)
        return(serie, descripcion)

    def incidencias_divisiones(self, RegCod: int):
        """
        Obtiene las incidencias de divisiones para una región dada.

        Parameters
        ----------
        RegCod : int
            Código de la región para la cual se desea obtener las incidencias de divisiones.

        Returns
        -------
        datos : List[Tuple[str, float]]
            Lista de tuplas que contienen el nombre de la división y su incidencia en la región especificada.
        descripcion : str
            Descripción textual de las incidencias de divisiones para la región especificada.
        """
        datos = self.SQL.incidencia_divisiones(RegCod)
        descripcion = self.Descriptor.incidencia_divisiones(datos)
        datos = Jo.invertir_orden(sorted(datos, reverse=True), Qfecha=False)
        return(datos, descripcion)
    
    def desagregacion_fuentes(self):
        datos = self.SQL.desagregacion_fuentes()
        descripcion = self.Descriptor.desagregacion_fuentes(datos, self.mes)
        return(datos, descripcion)

    def introduccion(self):
        inf_mensual = self.SQL.inflacion_mensual(self.anio, self.mes, 0)
        inf_interanual = self.SQL.inflacion_interanual(self.anio, self.mes, 0)
        inf_acumulada = self.SQL.inflacion_acumulada(self.anio, self.mes, 0)
        mes = Jo.mes_by_ordinal(self.mes, abreviado=False).lower()
        fecha = f"{mes} de {self.anio}"
        firma = """\\begin{center}
                    \\textbf{Brenda Izabel Miranda Consuegra}\\\\
                    Gerente\\\\
                    Instituto Nacional de Estadística
                    \\end{center}"""
        introduccion = f"""El presente informe mensual, contiene los principales
                        resultados del Índice de Precios al Consumidor (IPC) del
                        Instituto Nacional de Estadística (INE). Como indicador
                        macroeconómico, este dato se utiliza para medir el comportamiento
                        del nivel general de precios de la economía del país, tomando
                        como base los precios observados en el mes de referencia.\\\\\\\\

                        Los niveles de inflación más importantes de {fecha}
                        son los siguientes: se registró una inflación mensual de
                        {inf_mensual:.2f}\%, ritmo inflacionario de {inf_interanual:.2f}\%
                        y una inflación acumulada de {inf_acumulada:.2f}\%.\\\\\\\\

                        Este informe del IPC está compuesto de 11 apartados y 3 anexos.
                        En el primer apartado se incluyen los detalles del operativo de
                        campo, incluyendo la cobertura de fuentes y precios, la imputación
                        de precios y la desagregación de fuentes. En el segundo apartado,
                        se abordaron las variables exógenas, incluyendo el precio internacional
                        de los alimentos, el precio del petróleo, el cambio del quetzal,
                        la tasa de interés, entre otros. En el tercer apartado se presentan
                        los resultados del IPC, incluyendo la evolución del IPC, su variación
                        anual, acumulada y mensual, además de las incidencias mensuales
                        por división de gasto básico y los bienes con mayor impacto en
                        la variación mensual. Los apartados 4 a 11 incluyen resultados del
                        IPC para las regiones I a VIII.\\\\\\\\

                        Finalmente, para mayor comprensión del documento, se incluye
                        un anexo que contiene el glosario, con la definición de
                        los principales conceptos relacionados con el IPC, la metodología
                        de cálculo de las formulas más utilizadas para la obtención
                        de los diferentes índices y variaciones, y la evolución del IPC de
                        cada gasto básico. Y por último un anexo con las series históricas anuales
                        para cada gasto básico a nivel nacional.
                        {firma}"""
        return self.Descriptor.retocar_plantilla(introduccion)

    def cobertura_fuentes(self):
        datos = self.SQL.cobertura_fuentes_precios()
        descripcion = self.Descriptor.cobertura_fuentes(datos)
        return(datos, descripcion)

    def cobertura_precios(self):
        cobertura = self.SQL.cobertura_fuentes_precios(False)
        descripcion = self.Descriptor.cobertura_precios(cobertura)
        return(cobertura, descripcion)

    def ipc_regiones(self):
        datos = []
        for reg in range(1, 9):
            indice = self.SQL.calcular_IPC(self.anio, self.mes, reg)
            datos.append((reg, indice))
        descripcion = self.Descriptor.ipc_regiones(datos)
        return(datos, descripcion)

    def inflacion_interanual_regiones(self):
        datos = []
        for reg in range(1, 9):
            indice = self.SQL.inflacion_interanual(self.anio, self.mes, reg)
            datos.append((reg, indice))
        descripcion = self.Descriptor.inflacion_interanual_regiones(datos)
        return(datos, descripcion)

    def incidencias_gba(self, RegCod: int = 0, Qpositiva: bool = True):
        incidencias = sorted(self.SQL.incidencia_gasto_basico(RegCod), reverse=Qpositiva)
        incidencias = [i[::-1] for i in incidencias]
        top5 = incidencias[0:5]
        descripcion = self.Descriptor.incidencias_gba(top5, Qpositiva)
        return(top5, descripcion)
