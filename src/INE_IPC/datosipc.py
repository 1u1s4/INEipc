import xml.etree.ElementTree as ET
import requests
import json
import xlrd
from datetime import datetime
from fredapi import Fred
import funcionesjo as Jo
import descriptoripc
from bs4 import BeautifulSoup
from sqline import sqlINE
import pandas as pd

class datosIPC:
    def __init__(self, anio: int, mes: int) -> None:
        self._FORMATO = "%Y-%m-%d"
        self.mes = mes
        self.anio = anio
        self.SQL = sqlINE(anio, mes)

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
        for i in range(12):
            dato_i = df.iloc[i-13]
            fecha = dato_i['Date'].split('-')
            indice = dato_i['Food Price Index']
            fecha = Jo.mes_by_ordinal(fecha[1]) + '-' + fecha[0]
            data.append((fecha, indice))
        return(data, descriptoripc.indice_precio_alimentos(data))


    def petroleo(self, fecha_final="", fecha_inicial="") -> tuple:
        API_KEY ='734b605521e7734edc09f38e977fe238'
        SERIES_ID = 'DCOILWTICO'
        fred = Fred(api_key=API_KEY)
        if len(fecha_final) == 0:
            FECHA_FINAL = Jo.hoy(self._FORMATO)
        else:
            FECHA_FINAL = fecha_final
        if len(fecha_inicial) == 0:
            FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL)
        else:
            FECHA_INICIAL = fecha_inicial
        # carga de datos
        data = fred.get_series(
            series_id=SERIES_ID,
            observation_start=FECHA_INICIAL,
            bservation_end=FECHA_FINAL
        )
        # extraccion de los datos en el rango de fechas
        fecha_i = FECHA_INICIAL
        mes_actual = "-".join((fecha_i.split("-")[0], Jo.mes_by_ordinal(fecha_i.split("-")[1])))
        datos_mes = []
        data_mean = []
        while fecha_i != FECHA_FINAL:
            fecha_i = Jo.day_after(fecha_i)
            mes_actual_i = Jo.anio_mes(fecha_i)
            if mes_actual_i != mes_actual or fecha_i == FECHA_FINAL:
                mean = sum(datos_mes) / len(datos_mes)
                data_mean.append((mes_actual, mean))
                datos_mes = []
                mes_actual = mes_actual_i
            try:
                precio = data.dropna().loc[fecha_i]
                datos_mes.append(precio)
            except:
                None
        return (Jo.invertir_orden(data_mean), descriptoripc.petroleo(data_mean))

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
        return (Jo.invertir_orden(data_mean), descriptoripc.cambio_del_quetzal(data_mean))

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
        return (Jo.invertir_orden(data), descriptoripc.tasa_de_interes(data))

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
        return (Jo.invertir_orden(datos_variacion_interanual), descriptoripc.ipc_usa(datos_variacion_interanual))

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
        return(Jo.invertir_orden(datos_variacion_interanual), descriptoripc.ipc_mex(datos_variacion_interanual))

    def inflacion(self, fecha_final="", fecha_inicial="") -> tuple:
        if len(fecha_final) == 0:
            FECHA_FINAL = Jo.hoy(self._FORMATO)
        else:
            FECHA_FINAL = fecha_final
        if len(fecha_inicial) == 0:
            FECHA_INICIAL = Jo.year_ago(fecha=FECHA_FINAL, formato=self._FORMATO)
        else:
            FECHA_INICIAL = fecha_inicial
        # descarga de datos
        # GT (6,13) -> (6,14)
        book = xlrd.open_workbook("IPC C.A. REP. DOMINICANA Y MÉXICO.xlsx")
        sh = book.sheet_by_index(0)
        data = {}
        k = 0
        for i in range(6, 6 + 4*8, 4):
            pais = sh.cell_value(rowx=10, colx=2 + k*4)
            k += 1
            data_pais = {}
            for j in range(12):
                inflacion_ij = sh.cell_value(rowx=12 + j, colx= i - 1)
                data_pais[Jo.mes_by_ordinal(str(j + 1).rjust(2, "0"))] = inflacion_ij
            data[pais] = data_pais
        
        MES = Jo.mes_by_ordinal(FECHA_FINAL.split("-")[1])
        MES_ANTERIOR = Jo.mes_by_ordinal(FECHA_FINAL.split("-")[1], mes_anterior=True)
        ANIO = FECHA_FINAL.split("-")[0][2:4]
        data_salida = [("Pais", "-".join((MES, ANIO)), "-".join((MES_ANTERIOR, ANIO)))]
        for pais in data.keys():
            data_salida.append((pais.capitalize(), data[pais][MES], data[pais][MES_ANTERIOR]))
        return(data_salida, descriptoripc.inflacion(data, FECHA_FINAL))

# para el capitulo 3
    def serie_IPC(self, RegCod: int, QGba: bool = False):
        datos = self.SQL.serie_historica_ipc_pdr_adq(RegCod)
        descripcion = descriptoripc.serie_historica_ipc(datos, QGba)
        return(datos, descripcion)
    
    def serie_inflacion(self, RegCod: int, tipo: str, nivel: str='nacional'):
        datos = self.SQL.serie_historica_inflacion(RegCod, tipo)
        descripcion = descriptoripc.serie_historica_inflacion(datos, tipo, nivel)
        return(datos, descripcion)

    def serie_poder_adquisitivo(self, RegCod: int):
        datos = self.SQL.serie_historica_ipc_pdr_adq(RegCod, True)
        descripcion = descriptoripc.poder_adquisitivo(datos)
        return(datos, descripcion)

    def series_Gba(self, RegCod: int):
        salidas = [] # (NomGba, datos, descripcion)
        datos = self.SQL.series_historicas_Gbas(RegCod)
        for dt in datos:
            NomGba = dt[0] 
            datos_i = dt[1]
            descripcion = descriptoripc.serie_historica_ipc(dt, True)
            salidas.append((NomGba, datos_i, descripcion))
        return salidas
    
    def serie_fuentes(self):
        datos = self.SQL.serie_cobertura_fuentes()
        descripcion = descriptoripc.cobertura_fuentes(datos)
        return(datos, descripcion)

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
            descripcion = descriptoripc.cobertura_precios(serie)
        else:
            descripcion = descriptoripc.imputacion_precios(serie)
        return(serie, descripcion)

    def incidencias_divisiones(self, RegCod: int):
        datos = self.SQL.incidencia_divisiones(RegCod)
        descripcion = descriptoripc.incidencia_divisiones(datos)
        datos = Jo.invertir_orden(sorted(datos, reverse=True), Qfecha=False)
        return(datos, descripcion)