from typing import List
import warnings
warnings.filterwarnings("ignore")
import pyodbc 
import pandas as pd
import numpy as np
import os
from funcionesjo import mes_by_ordinal

class sqlINE:
    def __init__(self, anio: int, mes: int, QdbAux: bool=False, dbBackup: bool=False) -> None:
        self.__QdbAux = QdbAux
        self.anio = anio
        self.mes = mes
       # diccionario tipo de fuentes
        self.nombre_fuentes = {
            0: 'Sin tipo',#SIN TIPO DE FUENTE ASIGNADO
            1: 'Carnicerias',#CARNICERIAS, MARRANERIAS, POLLERIAS, ETC.
            2: 'Supermercados',#SUPERMERCADOS, DESPENSAS Y ALMACENES EN CADENA
            3: 'Hipermercados',#HIPERMERCADOS
            4: 'Depositos',#DEPOSITOS Y ABARROTERIAS
            5: 'Tiendas no Especializadas',#TIENDAS NO ESPECIALIZADAS (INCLUYE MISCELANEAS Y TIENDAS DE
            6: 'Almacenes',#ALMACENES O TIENDAS ESPECIALIZADAS
            7: 'Restaurantes',#RESTAURANTES  O EXPENDIOS DE COMIDAS PREPARADAS EN CADENA
            8: 'Empresas',#EMPRESAS ESPECIALIZADAS EN PRESTACION DE SERVICIOS
            9: 'Expendios de Gas',#EXPENDIOS DE GAS PROPANO
            10: 'Farmacias',#FARMACIAS, DROGUERIAS Y PERFUMERIAS
            11: 'Centros de Salud',#HOSPITALES, CLINICAS, CENTROS Y PUESTOS DE SALUD, LABORATORI
            12: 'Hoteles',#HOTELES, MOTELES, HOSPEDAJES, PENSIONES Y ALOJAMIENTOS
            13: 'Centros Educativos',#COLEGIOS, ACADEMIAS,  INSTITUTOS, UNIVERSIDADES Y OTROS
            14: 'Otros Establecimientos Especializados',#OTROS ESTABLECIMIENTOS ESPECIALIZADOS EN PREPARACION DE SERV
            15: 'Servicio Domestico',#SERVICIO DOMESTICO
            16: 'Otros Establecimientos No Especializados',#OTROS ESTABLECIMIENTOS NO ESPECIALIZADOS EN OTRO CODIGO
            20: 'Cuarto de Alquiler',#VIVIENDA TIPO CUARTO DE ALQUILER
            21: 'Apartamento de Alquiler',#VIVIENDA TIPO APARTAMENTO DE ALQUILER
            22: 'Casa de Alquiler',#VIVIENDA TIPO CASA DE ALQUILER
            23: 'Mercados',#MERCADOS CANTONALES Y MUNICIPALES ( COMPRA DE ALIMENTOS )
        }
        if dbBackup:
            self.df_DivInd = pd.read_feather('db_b/df_DivInd.feather')
            self.df_DivPon = pd.read_feather('db_b/df_DivPon.feather')
            self.df_GbaInd = pd.read_feather('db_b/df_GbaInd.feather')
            self.df_GbaPon = pd.read_feather('db_b/df_GbaPon.feather')
            self.df_GbaInfo = pd.read_feather('db_b/df_GbaInfo.feather')
            self.df_DivNom = pd.read_feather('db_b/df_DivNom.feather')
            self.df_Fnt = pd.read_feather('db_b/df_Fnt.feather')
        else:
            # datos servidor
            DATABASE = 'IPC2010_RN'
            SERVER = '10.0.0.3'
            USERNAME = 'lmdelgado'
            PASSWORD = 'Del/*2022'
            self.__conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}'
                + f';SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
            )
            self.df_DivNom = pd.read_sql(
                'SELECT DivCod, DivNom FROM IPCM01',
                self.__conexion
            )
            # ponderaciones de las divisiones
            self.df_DivPon = pd.read_sql(
                f'SELECT RegCod, DivCod, DivPon FROM IPCP01',
                self.__conexion
            )
            self.df_DivPon = self.df_DivPon.astype({'RegCod': 'int64', 'DivCod': 'int64'})
            # ponderaciones de los gastos basicos
            self.df_GbaPon = pd.read_sql(
                f'SELECT RegCod, DivCod, GbaCod, GbaPon FROM IPCP05',
                self.__conexion
            )
            columnas = ("RegCod", "DivCod", "GbaCod")
            self.df_GbaPon = self.df_GbaPon.astype(dict.fromkeys(columnas, "int64"))
            # informacion gastos basicos
            self.df_GbaInfo = pd.read_sql(
                'SELECT DivCod, AgrCod, GruCod, SubCod, GbaCod, GbaNom FROM IPCM05',
                self.__conexion
            )
            columnas = ('DivCod', 'AgrCod', 'GruCod', 'SubCod', 'GbaCod')
            self.df_GbaInfo = self.df_GbaInfo.astype(dict.fromkeys(columnas, "int64"))
            # indices por divicion
            self.df_DivInd = pd.read_sql(
                f'SELECT RegCod, PerAno, PerMes, DivCod, DivInd FROM IPCPH1 WHERE PerSem=3',
                self.__conexion
            )
            self.df_DivInd = self.df_DivInd.astype({"RegCod": "int64", "DivCod": "int64"})
            # indices por gasto basico
            self.df_GbaInd = pd.read_sql(
                f'SELECT RegCod, PerAno, PerMes, DivCod, AgrCod, GruCod, SubCod, GbaCod, GbaInd FROM IPCPH5 WHERE PerAno>={self.anio - 2} AND PerSem=3',
                self.__conexion
            )
            columnas = ('RegCod', 'PerAno', 'PerMes', 'DivCod', 'AgrCod', 'GruCod', 'SubCod', 'GbaCod')
            for columna in columnas:
                self.df_GbaInd[columna] = self.df_GbaInd[columna].astype('int64')
            # fuentes
            if self.__QdbAux:
                conexion_auxiliar = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server}'
                    + f';SERVER=INEVSQL01\A;DATABASE=master;UID=lmdelgado;PWD=Del/*2022'
                )
            else:
                conexion_auxiliar = self.__conexion
            query = f"""
SELECT * FROM (SELECT CASE 
        WHEN (H.ArtCod = 011110101 OR H.ArtCod = 011110102 OR H.ArtCod = 011110103) THEN 'ARROZ'
        WHEN (H.ArtCod = 011120305) THEN 'AVENA'
        WHEN (H.ArtCod = 011140102 OR H.ArtCod = 011140101 OR H.ArtCod = 011140103) THEN 'PASTAS ALIMENTICIAS'
        WHEN (H.ArtCod = 011130102) THEN 'PAN DULCE CORRIENTE O DE MANTECA'
        WHEN (H.ArtCod = 011130101) THEN 'PAN TIPO FRANCES'
        WHEN (H.ArtCod = 011150101) THEN 'TORTILLA DE MAIZ'
        WHEN (H.ArtCod  =011430103) THEN 'CREMA FRESCA'
        WHEN (H.ArtCod = 011410101) THEN 'LECHE EN POLVO'
        WHEN (H.ArtCod = 011410103 OR H.ArtCod = 011410102) THEN 'LECHE LIQUIDA'
        WHEN (H.ArtCod = 011430101) THEN 'QUESO FRESCO'
        WHEN (H.ArtCod = 011220103 OR H.ArtCod = 011220101) THEN 'CERDO SIN HUESO'
        WHEN (H.ArtCod = 011230102 OR H.ArtCod = 011230103 OR H.ArtCod = 011230101) THEN 'POLLO'
        WHEN (H.ArtCod = 011210105 OR H.ArtCod = 011210107) THEN 'CARNE DE RES CON HUESO'
        WHEN (H.ArtCod = 011210102 OR H.ArtCod = 011210103 OR H.ArtCod = 011210101 OR H.ArtCod = 011210106 OR H.ArtCod = 011210104) THEN 'CARNE DE RES SIN HUESO'
        WHEN (H.ArtCod = 011240101) THEN 'SALCHICHA'
        WHEN (H.ArtCod = 011440101) THEN 'HUEVOS DE GALLINA'
        WHEN (H.ArtCod = 011710802 OR H.ArtCod = 011710801) THEN 'FRIJOL NEGRO'
        WHEN (H.ArtCod = 011810101) THEN 'AZUCAR BLANCA GRANULADA'
        WHEN (H.ArtCod = 011520101) THEN 'ACEITE VEGETAL'
        WHEN (H.ArtCod = 011610101) THEN 'AGUACATE'
        WHEN (H.ArtCod = 011610201) THEN 'BANANO'
        WHEN (H.ArtCod = 011610603) THEN 'PIÑA'
        WHEN (H.ArtCod = 011610501) THEN 'PLATANOS'
        WHEN (H.ArtCod = 011610605) THEN 'SANDIAS'
        WHEN (H.ArtCod = 011711101) THEN 'CEBOLLA'
        WHEN (H.ArtCod = 011710201) THEN 'GUISQUIL'
        WHEN (H.ArtCod = 011712002) THEN 'HIERBAS FRESCAS'
        WHEN (H.ArtCod = 011711201) THEN 'PAPA'
        WHEN (H.ArtCod = 011710102 OR H.ArtCod = 011710101) THEN 'TOMATE'
        WHEN (H.ArtCod = 012130101) THEN 'AGUAS GASEOSAS'
        WHEN (H.ArtCod = 012110101 OR H.ArtCod = 012110201) THEN 'CAFÉ EN GRANO MOLIDO'
        WHEN (H.ArtCod = 011120304) THEN 'INCAPARINA'
        WHEN (H.ArtCod = 011910501) THEN 'SAL'
        WHEN (H.ArtCod = 011930301) THEN 'SOPAS INSTANTANEAS VASO'
        WHEN (H.ArtCod = 044210101) THEN 'GAS PROPANO'
        WHEN (H.ArtCod = 072210101) THEN 'GASOLINA SUPERIOR'
        WHEN (H.ArtCod = 072210201) THEN 'GASOLINA REGULAR'
        WHEN (H.ArtCod = 072210301) THEN 'DIESEL'
        ELSE 'No CBA'
    END AS 'Canasta Básica', H.PerAno, H.PerMes, H.PerSem, H.ArtCod, H.BolNum, H.ArtPac, H.ArtPhi, H.UreCan, H.UraChi, H.UmeCan, H.ArtCR, H.ArtSI, H.RegCod, H.ArtNOm, H.ArtPrc, H.TfnCod, H.TfnNom, H.FntCod, H.FntNom, H.DepCod, H.MunCod FROM 
(SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_01_RN.dbo.IPC104 a 
INNER JOIN IPC2010_01_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_01_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_01_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_01_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)
UNION ALL
SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_02_RN.dbo.IPC104 a 
INNER JOIN IPC2010_02_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem  AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_02_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_02_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_02_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)
UNION ALL 
SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_03_RN.dbo.IPC104 a 
INNER JOIN IPC2010_03_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem  AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_03_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_03_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_03_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)
UNION ALL 
SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_04_RN.dbo.IPC104 a 
INNER JOIN IPC2010_04_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem  AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_04_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_04_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_04_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)
UNION ALL 
SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_05_RN.dbo.IPC104 a 
INNER JOIN IPC2010_05_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem  AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_05_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_05_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_05_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)
UNION ALL 
SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_06_RN.dbo.IPC104 a 
INNER JOIN IPC2010_06_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem  AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_06_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_06_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_06_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)
UNION ALL 
SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_07_RN.dbo.IPC104 a 
INNER JOIN IPC2010_07_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem  AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_07_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_07_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_07_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)
UNION ALL 
SELECT a.PerAno, a.PerMes, a.PerSem, a.ArtCod, b.BolNum, a.ArtPac, a.ArtPhi, a.UreCan, a.UraChi, d.UmeCan, a.ArtCR, a.ArtSI, b.RegCod, d.ArtNOm, d.ArtPrc, e.TfnCod, e.TfnNom, c.FntCod, c.FntNom, b.DepCod, b.MunCod
FROM IPC2010_08_RN.dbo.IPC104 a 
INNER JOIN IPC2010_08_RN.dbo.IPC103 b ON (a.BolNum = b.BolNum AND a.PerAno = b.PerAno AND a.PerMes = b.PerMes AND a.PerSem = b.PerSem  AND a.RegCod = b.RegCod)
INNER JOIN IPC2010_08_RN.dbo.IPC010 c ON (c.FntCod = b.FntCod AND c.DepCod = b.DepCod AND c.MunCod =b.MunCod)
INNER JOIN IPC2010_08_RN.dbo.IPC007 d ON a.ArtCod = d.ArtCod
INNER JOIN IPC2010_08_RN.dbo.IPC008 e ON c.TfnCod = e.TfnCod
WHERE a.ArtCod IN (SELECT DISTINCT ArtCod FROM IPC2010_01_RN.dbo.IPCPH6 WHERE PerAno = 2010 AND PerMes = 12 AND ArtCod != 091110301)) H
WHERE H.PerAno >= {self.anio - 1}) J"""
            self.df_Fnt = pd.read_sql(query, conexion_auxiliar)
            columnas = ('RegCod', 'MunCod', 'DepCod', 'PerAno', 'PerMes')
            self.df_Fnt = self.df_Fnt.astype(dict.fromkeys(columnas, "int64"), errors='ignore')
        # fin de carga de datos 
        # nombre de divisiones
        abr_diviciones = {
            'Alimentos Y Bebidas No Alcohólicas': 'Alimentos',
            'Bebidas Alcohólicas Y Tabaco':'Bebidas Alcohólicas',
            'Prendas De Vestir Y Calzado':'Vestuario',
            'Vivienda, Agua, Electricidad, Gas Y Otros Combustibles':'Vivienda',
            'Muebles, Artículos Para El Hogar Y Para La Conservación  Del Hogar':'Muebles',
            'Salud':'Salud',
            'Transporte':'Transporte',
            'Comunicaciones':'Comunicaciones',
            'Recreación Y Cultura':'Recreación',
            'Educación':'Educación',
            'Restaurantes Y Hoteles':'Restaurantes',
            'Bienes Y Servicios Diversos':'Bienes diversos'
        }
        df_DivNom_dic = self.df_DivNom.to_dict()
        self.NOMBRE_DIV = dict(zip(
            [int(i) for i in df_DivNom_dic['DivCod'].values()],
            [abr_diviciones[nombre.strip().title()] for nombre in df_DivNom_dic['DivNom'].values()]
        ))

        # Comprobamos si la carpeta db_b existe
        if not os.path.exists("db_b"):
            # Si no existe, la creamos
            os.makedirs("db_b")
        self.df_DivInd.to_feather('db_b/df_DivInd.feather')
        self.df_DivPon.to_feather('db_b/df_DivPon.feather')
        self.df_GbaInd.to_feather('db_b/df_GbaInd.feather')
        self.df_GbaPon.to_feather('db_b/df_GbaPon.feather')
        self.df_GbaInfo.to_feather('db_b/df_GbaInfo.feather')
        self.df_DivNom.to_feather('db_b/df_DivNom.feather')
        self.df_Fnt.to_feather('db_b/df_Fnt.feather')

    def get_nombre_Gba(self, GbaCod: int) -> str:
        """
        Obtiene el nombre del gasto básico correspondiente al código proporcionado.

        Parameters
        ----------
        GbaCod : int
            Código del gasto básico para el cual se desea obtener el nombre.

        Returns
        -------
        str
            Nombre del gasto básico correspondiente al código proporcionado,
            con espacios iniciales y finales eliminados y en formato título.
        """
        nombre = self.df_GbaInfo[self.df_GbaInfo['GbaCod'] == GbaCod]['GbaNom'].iloc[0]
        return nombre.strip().title()

    def calcular_IPC(self, anio: int, mes: int, RegCod: int) -> float:
        """
        Calcula el índice de precios al consumidor (IPC) para una región y período de tiempo dados.

        Parameters
        ----------
        anio : int
            Año para el cual se desea calcular el IPC.
        mes : int
            Mes (número entero entre 1 y 12) para el cual se desea calcular el IPC.
        RegCod : int
            Código de la región para la cual se desea calcular el IPC.

        Returns
        -------
        float
            IPC calculado para la región y período de tiempo dados.
        """
        PONDERACIONES_REG = self.df_DivPon[self.df_DivPon['RegCod'] == RegCod]['DivPon']
        Qanio = self.df_DivInd['PerAno'] == anio
        Qmes = self.df_DivInd['PerMes'] == mes
        Qreg = self.df_DivInd['RegCod'] == RegCod
        indices = self.df_DivInd[Qanio & Qmes & Qreg]['DivInd']
        return np.average(a=indices, weights=PONDERACIONES_REG)

    def inflacion_mensual(self, anio: int, mes: int, RegCod: int) -> float:
        """
        Calcula la inflación mensual para una región específica.
        
        Parameters
        ----------
        anio : int
            El año para el cual se desea calcular la inflación.
        mes : int
            El mes para el cual se desea calcular la inflación, en formato numérico (1-12).
        RegCod : int
            El código de la región para la cual se desea calcular la inflación.
        
        Returns
        -------
        float
            El valor de la inflación mensual para la región y el periodo especificados, expresado como un porcentaje.
        """
        actual = self.calcular_IPC(anio, mes, RegCod)
        if mes == 1:
            anterior = self.calcular_IPC(anio - 1, 12, RegCod)
        else:
            anterior = self.calcular_IPC(anio, mes - 1, RegCod)
        return 100*(actual/anterior - 1)

    def inflacion_interanual(self, anio: int, mes: int, RegCod: int) -> float:
        actual = self.calcular_IPC(anio, mes, RegCod)
        anterior = self.calcular_IPC(anio - 1, mes, RegCod)
        return 100*(actual/anterior - 1)
    
    def inflacion_acumulada(self, anio: int, mes: int, RegCod: int) -> float:
        actual = self.calcular_IPC(anio, mes, RegCod)
        anterior = self.calcular_IPC(anio - 1, 12, RegCod)
        return 100*(actual/anterior - 1)
    
    def poder_adquisitivo(self, anio: int, mes: int, RegCod: int) -> float:
        return (1 / self.calcular_IPC(anio, mes, RegCod)) * 100

    def incidencia_divisiones(self, RegCod: int) -> List[float]:
        incidencias = []
        for DivCod in range(1, 13):
            ponderacion = self.df_DivPon[(self.df_DivPon['RegCod'] == RegCod) & (self.df_DivPon['DivCod'] == DivCod)]['DivPon'].iloc[0]
            Qanio = self.df_DivInd['PerAno'] == self.anio
            Qmes = self.df_DivInd['PerMes'] == self.mes
            Qreg = self.df_DivInd['RegCod'] == RegCod
            Qdiv = self.df_DivInd['DivCod'] == DivCod
            indice_actual = self.df_DivInd[Qanio & Qmes & Qreg & Qdiv]['DivInd'].iloc[0]
            if self.mes == 1:
                Qanio = self.df_DivInd['PerAno'] == self.anio - 1
                Qmes = self.df_DivInd['PerMes'] == 12
                ipc_anterior = self.calcular_IPC(self.anio - 1, 12, RegCod)
            else:
                Qmes = self.df_DivInd['PerMes'] == self.mes - 1
                ipc_anterior = self.calcular_IPC(self.anio, self.mes - 1, RegCod)
            indice_anterior = self.df_DivInd[Qanio & Qmes & Qreg & Qdiv]['DivInd'].iloc[0]
            variacion = ((indice_actual - indice_anterior) / ipc_anterior) * ponderacion
            incidencias.append((variacion, self.NOMBRE_DIV[DivCod]))
        return incidencias

    def incidencia_gasto_basico(self, RegCod: int):
        incidencias = []
        for GbaCod in self.df_GbaInfo['GbaCod'].to_list():
            ponderacion = self.df_GbaPon[(self.df_GbaPon['RegCod'] == RegCod) & (self.df_GbaPon['GbaCod'] == GbaCod)]['GbaPon'].iloc[0]
            Qanio = self.df_GbaInd['PerAno'] == self.anio
            Qmes = self.df_GbaInd['PerMes'] == self.mes
            Qreg = self.df_GbaInd['RegCod'] == RegCod
            Qgba = self.df_GbaInd['GbaCod'] == GbaCod
            try:
                indice_actual = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba]['GbaInd'].iloc[0]
            except:
                pass
            if self.mes == 1:
                Qanio = self.df_GbaInd['PerAno'] == self.anio - 1
                Qmes = self.df_GbaInd['PerMes'] == 12
                ipc_anterior = self.calcular_IPC(self.anio - 1, 12, RegCod)
            else:
                Qmes = self.df_GbaInd['PerMes'] == self.mes - 1
                ipc_anterior = self.calcular_IPC(self.anio, self.mes - 1, RegCod)
            try:
                indice_anterior = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba]['GbaInd'].iloc[0]
            except:
                pass
            variacion = ((indice_actual - indice_anterior) / ipc_anterior) * ponderacion
            nombre_gba = self.get_nombre_Gba(GbaCod)
            incidencias.append((variacion, nombre_gba))
        return incidencias

    def series_historicas_Gbas(self, RegCod: int):
        series = []
        for GbaCod in self.df_GbaInfo['GbaCod'].to_list():
            if self.mes != 12:
                Qanio = self.df_GbaInd['PerAno'] == self.anio
                Qmes = self.df_GbaInd['PerMes'] <= self.mes
                Qreg = self.df_GbaInd['RegCod'] == RegCod
                Qgba = self.df_GbaInd['GbaCod'] == GbaCod
                #Qsem = self.df_GbaInd['PerSem'] == 3
                indices1 = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba][['PerAno','PerMes','GbaInd']]
                Qanio = self.df_GbaInd['PerAno'] == self.anio - 1
                Qmes = self.df_GbaInd['PerMes'] >= self.mes
                indices2 = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba][['PerAno','PerMes','GbaInd']]
                indices = pd.merge(indices2, indices1, how='outer')
            else:
                Qanio = self.df_GbaInd['PerAno'] == self.anio
                Qmes = self.df_GbaInd['PerMes'] <= self.mes
                Qreg = self.df_GbaInd['RegCod'] == RegCod
                Qgba = self.df_GbaInd['GbaCod'] == GbaCod
                #Qsem = self.df_GbaInd['PerSem'] == 3
                indices = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba][['PerAno','PerMes','GbaInd']]
            nombre_gba = self.get_nombre_Gba(GbaCod)
            indices_final = []
            if len(indices) != 0:
                for i in range(len(indices)):
                    mes_abr = mes_by_ordinal(indices['PerMes'].iat[i])
                    anio = indices['PerAno'].iat[i]
                    fecha = f'{mes_abr}-{anio}'
                    indice = indices['GbaInd'].iat[i]
                    indices_final.append((fecha, indice))
                series.append((nombre_gba, indices_final))
        return series

    def serie_historica_ipc_pdr_adq(self, RegCod: int, Qpdr_adq: bool=False):
        serie = []
        if Qpdr_adq:
            funcion = self.poder_adquisitivo
        else:
            funcion = self.calcular_IPC
        if self.mes != 12:
            for i in range(self.mes, 13):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio - 1}'
                ipc = funcion(self.anio - 1, i, RegCod)
                serie.append((fecha, ipc))
            for i in range(1, self.mes + 1):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                ipc = funcion(self.anio, i, RegCod)
                serie.append((fecha, ipc))
        else:
            for i in range(1, 13):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                ipc = funcion(self.anio, i, RegCod)
                serie.append((fecha, ipc))
        return serie

    def serie_historica_inflacion(self, RegCod: int, tipo: str):
        serie = []
        if tipo == 'intermensual':
            funcion = self.inflacion_mensual
        elif tipo == 'interanual':
            funcion = self.inflacion_interanual
        elif tipo == 'acumulada':
            funcion = self.inflacion_acumulada
        if tipo == 'acumulada':
            for anio in range(2012, self.anio + 1):
                mes_abr = mes_by_ordinal(self.mes)
                fecha = f'{mes_abr}-{anio}'
                indice = funcion(anio, self.mes, RegCod)
                serie.append((fecha, indice))
        else:
            if self.mes != 12:
                for i in range(self.mes, 13):
                    mes_abr = mes_by_ordinal(i)
                    fecha = f'{mes_abr}-{self.anio - 1}'
                    indice = funcion(self.anio - 1, i, RegCod)
                    serie.append((fecha, indice))
                for i in range(1, self.mes + 1):
                    mes_abr = mes_by_ordinal(i)
                    fecha = f'{mes_abr}-{self.anio}'
                    indice = funcion(self.anio, i, RegCod)
                    serie.append((fecha, indice))
            else:
                for i in range(1, 13):
                    mes_abr = mes_by_ordinal(i)
                    fecha = f'{mes_abr}-{self.anio}'
                    indice = funcion(self.anio, i, RegCod)
                    serie.append((fecha, indice))
        return serie

    def serie_fuentes_precios(self, Qfuentes: bool = True):
        serie = []
        if self.mes != 12:
            for i in range(self.mes, 13):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio - 1}'
                mes_ = self.df_Fnt['PerMes'] == i
                anio_ = self.df_Fnt['PerAno'] == self.anio - 1
                conteo = self.df_Fnt[anio_ & mes_]
                if Qfuentes:
                    conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
                serie.append((fecha, conteo.shape[0]))
            for i in range(1, self.mes + 1):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = self.df_Fnt['PerMes'] == i
                anio_ = self.df_Fnt['PerAno'] == self.anio
                conteo = self.df_Fnt[anio_ & mes_]
                if Qfuentes:
                    conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
                serie.append((fecha, conteo.shape[0]))
        else:
            for i in range(1, 13):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = self.df_Fnt['PerMes'] == i
                anio_ = self.df_Fnt['PerAno'] == self.anio
                conteo = self.df_Fnt[anio_ & mes_]
                if Qfuentes:
                    conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
                serie.append((fecha, conteo.shape[0]))
        return serie

    def desagregacion_fuentes(self):
        serie = []
        mes_ = self.df_Fnt['PerMes'] == self.mes
        anio_ = self.df_Fnt['PerAno'] == self.anio
        S = 1
        for i in range(24):
            if i in (17,18,19): # no existen estos tipos de fuentes
                continue
            tipo_fuente_ = self.df_Fnt['TfnCod'] == str(i).zfill(2)
            conteo = self.df_Fnt[anio_ & mes_ & tipo_fuente_].shape[0]
            S += conteo
            nmbr_Fnt = self.nombre_fuentes.get(i)
            serie.append((nmbr_Fnt, conteo))
        invertir = [(i[1] / S * 100, i[0]) for i in serie]
        serie = [i[::-1] for i in sorted(invertir, reverse=True)]
        # hacer pareto
        acumulado = 0
        for i, fuente in enumerate(serie):
            acumulado += fuente[1]
            if acumulado >= 80:
                break
        return serie[0:i + 1]
    
    def cobertura_fuentes_precios(self, Qfuentes: bool = True):
        cobertura = []
        mes_ = self.df_Fnt['PerMes'] == self.mes
        anio_ = self.df_Fnt['PerAno'] == self.anio
        for i in range(1, 9):
            RegCod_ = self.df_Fnt['RegCod'] == i
            conteo = self.df_Fnt[anio_ & mes_ & RegCod_]
            if Qfuentes:
                conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
            cobertura.append((i, conteo.shape[0]))
        return cobertura

    def serie_historica(self, tipo: str, Qtabla: bool=False):
        serie = []
        funcion = self.inflacion_mensual if tipo == 'intermensual' else self.inflacion_interanual
        anio_inf = 2011 if tipo == 'intermensual' else 2012
        J = 0 # para corregir las etiquetas
        for anio in range(anio_inf, self.anio):
            for mes in range(1, 13):
                J += 1
                indice = funcion(anio, mes, 0)
                if Qtabla:
                    mes_abr = mes_by_ordinal(mes, False)
                    serie.append((anio, mes_abr, indice))
                else:
                    mes_abr = mes_by_ordinal(mes)
                    fecha = f'{mes_abr}-{anio}'
                    serie.append((fecha, indice))
        for mes in range(1, self.mes + 1):
                J += 1
                indice = funcion(self.anio, mes, 0)
                if Qtabla:
                    mes_abr = mes_by_ordinal(mes, False)
                    serie.append((self.anio, mes_abr, indice))
                else:
                    mes_abr = mes_by_ordinal(mes)
                    fecha = f'{mes_abr}-{self.anio}'
                    serie.append((fecha, indice))
        return serie
