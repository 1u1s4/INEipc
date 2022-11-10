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

class datosIPC:
    def __init__(self, anio: int, mes: int) -> None:
        self._FORMATO = "%Y-%m-%d"
        self.mes = mes
        self.anio = anio
        self.SQL = sqlINE(anio, mes)
        self.Descriptor = Descriptor(anio, mes) 

    def indice_precio_alimentos(self) -> tuple:
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

    def __petroleo_series_mean(self, anio, mes):
        API_KEY ='734b605521e7734edc09f38e977fe238'
        SERIES_ID = 'DCOILWTICO'
        fred = Fred(api_key=API_KEY)
        FECHA_INICIAL = f"{anio}-{mes}-01"
        if mes in (1, 3, 5, 7, 8, 10, 12):
            ultimo_dia = 31
        elif mes == 2:
            ultimo_dia = 28
        else:
            ultimo_dia = 30
        FECHA_FINAL = f"{anio}-{mes}-{ultimo_dia}"
        # carga de datos
        data = fred.get_series(
            series_id=SERIES_ID,
            observation_start=FECHA_INICIAL,
            observation_end=FECHA_FINAL
        )
        data = data.dropna()
        return data.mean()

    def petroleo(self) -> tuple:
        # extraccion de los datos en el rango de fechas
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

    def cambio_quetzal(self, fecha_final="", fecha_inicial="") -> tuple:
        FORMATO = "%d/%m/%Y"
        if len(fecha_final) == 0:
            FECHA_FINAL = Jo.hoy(FORMATO)
        else:
            FECHA_FINAL = Jo.ultimo_dia_del_mes(fecha=fecha_final, formato=FORMATO)
        if len(fecha_inicial) == 0:
            FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL, formato=FORMATO, inicio_de_mes=True)
        else:
            FECHA_INICIAL = fecha_inicial
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
        mes_actual = "-".join((fecha_i.split("/")[2], Jo.mes_by_ordinal(fecha_i.split("/")[1])))
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

    def tasa_interes(self, fecha_final="", fecha_inicial="") -> tuple:
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
        for i in range(int(FECHA_INICIAL.split("-")[1]) + 4, 12 + 5):
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

    def ipc_usa(self, fecha_final="", fecha_inicial="") -> tuple:
        if len(fecha_final) == 0:
            FECHA_FINAL = Jo.hoy(self._FORMATO, inicio_de_mes=True)
        else:
            FECHA_FINAL = fecha_final
        if len(fecha_inicial) == 0:
            FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL)
        else:
            FECHA_INICIAL = fecha_inicial
        FECHA_INICIAL_INICIAL = Jo.year_ago(fecha=FECHA_INICIAL, inicio_de_anio=True)
        API_KEY = '734b605521e7734edc09f38e977fe238'
        fred = Fred(api_key=API_KEY)
        data = fred.get_series('CPIAUCSL', observation_start=FECHA_INICIAL_INICIAL, observation_end=FECHA_FINAL)
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

    def ipc_mex(self, fecha_final="", fecha_inicial="") -> tuple:
        if len(fecha_final) == 0:
            FECHA_FINAL = Jo.hoy(self._FORMATO)
        else:
            FECHA_FINAL = fecha_final
        if len(fecha_inicial) == 0:
            FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL)
        else:
            FECHA_INICIAL = fecha_inicial
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

    def inflacion_CA_RD_MEX(self):
        paises = ("Guatemala", "El Salvador", "Honduras", "Nicaragua", "Costa Rica", "Republica Dominicana", "Panama", "Mexico")
        mes = Jo.mes_by_ordinal(self.mes)
        data = [("Pais", f"{mes}-{self.anio}", f"{mes}-{self.anio}")]
        mes_actual = Jo.mes_by_ordinal(self.mes - 1, abreviado=False)
        mes_anterior = Jo.mes_by_ordinal(self.mes - 2, abreviado=False)
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
            # inflacion interanual del mes anterior
            mes_ = df["mes"] == mes_anterior
            anio_ = df["anio"] == self.anio
            indice_actual = df[mes_ & anio_]["indice"].iloc[0]
            mes_ = df["mes"] == mes_anterior
            anio_ = df["anio"] == (self.anio - 1)
            indice_anterior = df[mes_ & anio_]["indice"].iloc[0]
            inflacion_anterior = (indice_actual/indice_anterior - 1) * 100 
            data.append((pais, inflacion_actual, inflacion_anterior))
        return (data, self.Descriptor.inflacion(data, mes_actual.lower(), self.anio))

# para el capitulo 3
    def serie_IPC(self, RegCod: int, QGba: bool = False):
        datos = self.SQL.serie_historica_ipc_pdr_adq(RegCod)
        descripcion = self.Descriptor.serie_historica_ipc(datos, QGba)
        return(datos, descripcion)
    
    def serie_inflacion(self, RegCod: int, tipo: str, nivel: str='nacional'):
        datos = self.SQL.serie_historica_inflacion(RegCod, tipo)
        descripcion = self.Descriptor.serie_historica_inflacion(datos, tipo, nivel)
        return(datos, descripcion)

    def serie_poder_adquisitivo(self, RegCod: int):
        datos = self.SQL.serie_historica_ipc_pdr_adq(RegCod, True)
        descripcion = self.Descriptor.poder_adquisitivo(datos)
        return(datos, descripcion)

    def series_Gba(self, RegCod: int):
        salidas = [] # (NomGba, datos, descripcion)
        datos = self.SQL.series_historicas_Gbas(RegCod)
        for dt in datos:
            NomGba = dt[0] 
            datos_i = dt[1]
            descripcion = self.Descriptor.serie_historica_ipc(dt, True)
            salidas.append((NomGba, datos_i, descripcion))
        return salidas
    
    def serie_fuentes(self):
        datos = self.SQL.serie_cobertura_fuentes()
        descripcion = self.Descriptor.cobertura_fuentes(datos)
        return(datos, descripcion)

    def cobertura_precios(self):
        cobertura = []
        df = pd.read_excel('BASE DE DATOS PERIODOS DE ESPERA POR DECADA.xlsx', sheet_name=1).fillna(0)
        anio_ = df['Año'] == self.anio
        mes_ = df['Mes'] == self.mes
        df = df[anio_ & mes_]
        for i in range(1, 9):
            region_ = df['Región'] == i
            df_i = df[region_].reset_index()
            suma = 0
            for j in range(len(df_i)):
                try:
                    precios_prediligenciados = int(df_i.loc[j]['Prec_Pre'])
                except:
                    precios_prediligenciados = 0
                suma += precios_prediligenciados
            cobertura.append((i, suma))
        descripcion = self.Descriptor.cobertura_precios(cobertura)
        return(cobertura, descripcion)

    def serie_precios(self, Qcobertura: bool=False):
        serie = []
        df = pd.read_excel('BASE DE DATOS PERIODOS DE ESPERA POR DECADA.xlsx', sheet_name=1).fillna(0)
        if self.mes == 12:
            for i in range(1, 13):
                mes_abr = Jo.mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = df['Mes'] == i
                anio_ = df['Año'] == self.anio
                df_i = df[mes_ & anio_].reset_index()
                suma = 0
                for j in range(len(df_i)):
                    try:
                        precios_espera = int(df_i.loc[j]['Prec_PE'])
                    except:
                        precios_espera = 0
                    try:
                        precios_recuperados = int(df_i.loc[j]['Prec_Recup'])
                    except:
                        precios_recuperados = 0
                    if Qcobertura:
                        try:
                            precios_prediligenciados = int(df_i.loc[j]['Prec_Pre'])
                        except:
                            precios_prediligenciados = 0
                        suma += precios_prediligenciados
                    else:
                        suma += precios_espera - precios_recuperados
                serie.append((fecha, abs(suma)))
        else:
            for i in range(self.mes, 13):
                mes_abr = Jo.mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio - 1}'
                mes_ = df['Mes'] == i
                anio_ = df['Año'] == self.anio - 1
                df_i = df[mes_ & anio_].reset_index()
                suma = 0
                for j in range(len(df_i)):
                    try:
                        precios_espera = int(df_i.loc[j]['Prec_PE'])
                    except:
                        precios_espera = 0
                    try:
                        precios_recuperados = int(df_i.loc[j]['Prec_Recup'])
                    except:
                        precios_recuperados = 0
                    if Qcobertura:
                        try:
                            precios_prediligenciados = int(df_i.loc[j]['Prec_Pre'])
                        except:
                            precios_prediligenciados = 0
                        suma +=precios_prediligenciados
                    else:
                        suma += precios_espera - precios_recuperados
                serie.append((fecha, abs(suma)))
            for i in range(1, self.mes + 1):
                mes_abr = Jo.mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = df['Mes'] == i
                anio_ = df['Año'] == self.anio
                df_i = df[mes_ & anio_].reset_index()
                suma = 0
                for j in range(len(df_i)):
                    try:
                        precios_espera = int(df_i.loc[j]['Prec_PE'])
                    except:
                        precios_espera = 0
                    try:
                        precios_recuperados = int(df_i.loc[j]['Prec_Recup'])
                    except:
                        precios_recuperados = 0
                    if Qcobertura:
                        try:
                            precios_prediligenciados = int(df_i.loc[j]['Prec_Pre'])
                        except:
                            precios_prediligenciados = 0
                        suma +=precios_prediligenciados
                    else:
                        suma += precios_espera - precios_recuperados
                serie.append((fecha, abs(suma)))
        if Qcobertura:
            descripcion = self.Descriptor.serie_precios(serie)
        else:
            descripcion = self.Descriptor.imputacion_precios(serie)
        return(serie, descripcion)

    def incidencias_divisiones(self, RegCod: int):
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
        introduccion = f"""El presente informe mensual, contiene los principales
                        resultados del Índice de Precios al Consumidor (IPC) del
                        Instituto Nacional de Estadística (INE). Como indicador
                        macroeconómico, este dato se utiliza para medir el comportamiento
                        del nivel general de precios de la economía del país, tomando
                        como base los precios observados en el mes de referencia.NTR

                        Los niveles de inflación más importantes de {fecha}
                        son los siguientes: se registró una inflación mensual de
                        {inf_mensual:.2f}\%, ritmo inflacionario de {inf_interanual:.2f}\%
                        y una inflación acumulada de {inf_acumulada:.2f}\%.\\\\\\\\

                        Este informe se compone de seis apartados y tres anexos: el
                        primero incluye el número índice y los resultados de las
                        inflaciones mensuales, acumuladas e interanuales a nivel
                        república, en el segundo se exponen las variaciones mensuales
                        históricas, por región y por división de gasto, en el tercero
                        se muestran los ritmos inflacionarios históricos, por región
                        y por división de gasto, en el cuarto se presentan las
                        principales alzas y bajas de los productos que conforman el
                        IPC y su incidencia en la inflación mensual; en el quinto se
                        describen las principales alzas y bajas de los productos que
                        conforman el IPC y su incidencia en el ritmo inflacionario;
                        en el sexto se consigna la evolución del poder adquisitivo del
                        quetzal; anexo 1: tablas de índices e inflaciones por región
                        y por división de gasto.\\\\\\\\

                        Finalmente, para mayor comprensión del documento, se incluye
                        un anexo 2 y 3 que contiene el glosario, con la definición de
                        los principales conceptos relacionados con el IPC y la metodología
                        de cálculo de las formulas más utilizadas para la obtención
                        de los diferentes índices y variaciones."""
        return self.Descriptor.retocar_plantilla(introduccion)

    def cobertura_fuentes(self):
        datos = self.SQL.cobertura_fuentes()
        print(datos)
