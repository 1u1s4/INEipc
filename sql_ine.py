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
        # carga nombre de divisiones
        sql_query = pd.read_sql(
            'SELECT DivCod, DivNom FROM IPCM01',
            self.__conexion
        ).to_dict()
        self.NOMBRE_DIV = dict(zip(
            sql_query['DivCod'].values(),
            [nombre.strip().title() for nombre in sql_query['DivNom'].values()]
        ))
        # cargar ponderaciones de las divisiones para una region dada
        self.DivPon = pd.read_sql(
            f'SELECT RegCod, DivCod, DivPon FROM IPCP01',
            self.__conexion
        )
        self.DivPon['RegCod'] = self.DivPon['RegCod'].astype('int64')
        # carga de indices por divicion
        self.DivInd = pd.read_sql(
            f'SELECT RegCod, PerAno, PerMes, DivCod, DivInd FROM IPCPH1 WHERE PerAno>={anio - 1} AND PerSem=3',
            self.__conexion
        )
        self.DivInd['RegCod'] = self.DivInd['RegCod'].astype('int64')
        self.DivInd['DivCod'] = self.DivInd['DivCod'].astype('int64')

    def calcular_IPC(self, anio: int, mes: int, RegCod: int) -> float:
        PONDERACIONES_REG = self.DivPon[self.DivPon['RegCod'] == RegCod]['DivPon']
        Qanio = self.DivInd['PerAno'] == anio
        Qmes = self.DivInd['PerMes'] == mes
        Qreg = self.DivInd['RegCod'] == RegCod
        indices = self.DivInd[Qanio & Qmes & Qreg]['DivInd']
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

p = sqlINE(2022)
print(p.inflacion_mensual(2022, 8,0))