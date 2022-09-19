from typing import List
import warnings
warnings.filterwarnings("ignore")
import pyodbc 
import pandas as pd
import numpy as np

class sqlINE:
    def __init__(self, anio: int) -> None:
        # datos servidor
        DATABASE = 'IPC2010_RN'
        SERVER = '10.0.3.185'
        USERNAME = 'laalvarado'
        PASSWORD = 'Abc$2022'
        self.__conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}'
            + f';SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        )
        # nombre de divisiones
        sql_query = pd.read_sql(
            'SELECT DivCod, DivNom FROM IPCM01',
            self.__conexion
        ).to_dict()
        self.NOMBRE_DIV = dict(zip(
            sql_query['DivCod'].values(),
            [nombre.strip().title() for nombre in sql_query['DivNom'].values()]
        ))
        # ponderaciones de las divisiones
        self.df_DivPon = pd.read_sql(
            f'SELECT RegCod, DivCod, DivPon FROM IPCP01',
            self.__conexion
        )
        self.df_DivPon['RegCod'] = self.df_DivPon['RegCod'].astype('int64')
        self.df_DivPon['DivCod'] = self.df_DivPon['DivCod'].astype('int64')
        # ponderaciones de los gastos basicos
        self.df_GbaPon = pd.read_sql(
            f'SELECT RegCod, DivCod, GbaCod, GbaPon FROM IPCP05',
            self.__conexion
        )
        self.df_GbaPon['RegCod'] = self.df_GbaPon['RegCod'].astype('int64')
        self.df_GbaPon['DivCod'] = self.df_GbaPon['DivCod'].astype('int64')
        self.df_GbaPon['GbaCod'] = self.df_GbaPon['GbaCod'].astype('int64')
        # informacion gastos basicos
        self.df_GbaInfo = pd.read_sql(
            'SELECT DivCod, AgrCod, GruCod, SubCod, GbaCod, GbaNom FROM IPCM05',
            self.__conexion
        )
        columnas = ('DivCod', 'AgrCod', 'GruCod', 'SubCod', 'GbaCod')
        for columna in columnas:
            self.df_GbaInfo[columna] = self.df_GbaInfo[columna].astype('int64')
        # indices por divicion
        self.df_DivInd = pd.read_sql(
            f'SELECT RegCod, PerAno, PerMes, DivCod, DivInd FROM IPCPH1 WHERE PerAno>={anio - 1} AND PerSem=3',
            self.__conexion
        )
        self.df_DivInd['RegCod'] = self.df_DivInd['RegCod'].astype('int64')
        self.df_DivInd['DivCod'] = self.df_DivInd['DivCod'].astype('int64')
        # indices por gasto basico
        self.df_GbaInd = pd.read_sql(
            f'SELECT RegCod, PerAno, PerMes, DivCod, AgrCod, GruCod, SubCod, GbaCod, GbaInd FROM IPCPH5 WHERE PerAno>={anio - 1}',
            self.__conexion
        )
        columnas = ('RegCod', 'PerAno', 'PerMes', 'DivCod', 'AgrCod', 'GruCod', 'SubCod', 'GbaCod')
        for columna in columnas:
            self.df_GbaInd[columna] = self.df_GbaInd[columna].astype('int64')

    def calcular_IPC(self, anio: int, mes: int, RegCod: int) -> float:
        PONDERACIONES_REG = self.df_DivPon[self.df_DivPon['RegCod'] == RegCod]['DivPon']
        Qanio = self.df_DivInd['PerAno'] == anio
        Qmes = self.df_DivInd['PerMes'] == mes
        Qreg = self.df_DivInd['RegCod'] == RegCod
        indices = self.df_DivInd[Qanio & Qmes & Qreg]['DivInd']
        return np.average(a=indices, weights=PONDERACIONES_REG)

    def inflacion_mensual(self, anio: int, mes: int, RegCod: int) -> float:
        if mes == 1:
            actual = self.calcular_IPC(anio, mes, RegCod)
            anterior = self.calcular_IPC(anio - 1, 12, RegCod)
        else:
            actual = self.calcular_IPC(anio, mes, RegCod)
            anterior = self.calcular_IPC(anio, mes - 1, RegCod)
        return 100*(actual/anterior - 1)

    def inflacion_interanual(self, anio: int, mes: int, RegCod: int) -> float:
        actual = self.calcular_IPC(anio, mes, RegCod)
        anterior = self.calcular_IPC(anio - 1, mes, RegCod)
        return 100*(actual/anterior - 1)
    
    def poder_adquisitivo(self, anio: int, mes: int, RegCod: int) -> float:
        return (1 / self.calcular_IPC(anio, mes, RegCod)) * 100
#INCIDENCIAS MALAS
    def incidencia_divisiones(self, anio: int, mes: int, RegCod: int) -> List[float]:
        incidencias = []
        for DivCod in range(1, 13):
            ponderacion = self.df_DivPon[(self.df_DivPon['RegCod'] == RegCod) & (self.df_DivPon['DivCod'] == DivCod)]['DivPon'].iloc[0]
            Qanio = self.df_DivInd['PerAno'] == anio
            Qmes = self.df_DivInd['PerMes'] == mes
            Qreg = self.df_DivInd['RegCod'] == RegCod
            Qdiv = self.df_DivInd['DivCod'] == DivCod
            indice_actual = self.df_DivInd[Qanio & Qmes & Qreg & Qdiv]['DivInd'].iloc[0]
            if mes == 1:
                Qanio = self.df_DivInd['PerAno'] == anio - 1
                ipc_anterior = self.calcular_IPC(anio - 1, mes, RegCod)
            else:
                Qmes = self.df_DivInd['PerMes'] == mes - 1
                ipc_anterior = self.calcular_IPC(anio, mes - 1, RegCod)
            indice_anterior = self.df_DivInd[Qanio & Qmes & Qreg & Qdiv]['DivInd'].iloc[0]
            variacion = ((indice_actual - indice_anterior) / ipc_anterior) * ponderacion
            incidencias.append((variacion, DivCod))
        return incidencias
#INCIDENCIAS MALAS
    def incidencia_gasto_basico(self, anio: int, mes: int, RegCod: int):
        incidencias = []
        for GbaCod in self.df_GbaInfo['GbaCod'].to_list():
            ponderacion = self.df_GbaPon[(self.df_GbaPon['RegCod'] == RegCod) & (self.df_GbaPon['GbaCod'] == GbaCod)]['GbaPon'].iloc[0]
            Qanio = self.df_GbaInd['PerAno'] == anio
            Qmes = self.df_GbaInd['PerMes'] == mes
            Qreg = self.df_GbaInd['RegCod'] == RegCod
            Qgba = self.df_GbaInd['GbaCod'] == GbaCod
            indice_actual = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba]['GbaInd'].iloc[0]
            if mes == 1:
                Qanio = self.df_GbaInd['PerAno'] == anio - 1
                ipc_anterior = self.calcular_IPC(anio - 1, mes, RegCod)
            else:
                Qmes = self.df_GbaInd['PerMes'] == mes - 1
                ipc_anterior = self.calcular_IPC(anio, mes - 1, RegCod)
            indice_anterior = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba]['GbaInd'].iloc[0]
            variacion = ((indice_actual - indice_anterior) / ipc_anterior) * ponderacion
            nombre_gba = self.df_GbaInfo[self.df_GbaInfo['GbaCod'] == GbaCod]['GbaNom'].iloc[0]
            nombre_gba = nombre_gba.strip().title()
            incidencias.append((round(variacion,2), nombre_gba))
        return incidencias

anio = 2022
p = sqlINE(anio)
print(sorted(p.incidencia_gasto_basico(anio, 8, 0))[-5:-1])