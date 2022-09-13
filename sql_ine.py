import warnings
warnings.filterwarnings("ignore")
import pyodbc 
import pandas as pd
import numpy as np

class sqlINE:
    def __init__(self) -> None:
        # datos servidor
        DATABASE = 'IPC2010_RN'
        SERVER = '10.0.3.185'
        USERNAME = 'laalvarado'
        PASSWORD = 'Abc$2022'
        self.__conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}'
            + f';SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        )
        # cargar ponderaciones de las divisiones
        self.PONDERACIONES_DIV = pd.read_sql(
            'SELECT DivCod, DivPon FROM IPCP01 WHERE RegCod=00',
            self.__conexion
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
        
    def carga_DivInd(self, anio: int, mes: int) -> pd.DataFrame:
        SELECT = 'SELECT DivCod, DivInd'
        FROM = 'FROM IPCPH1'
        WHERE = f'WHERE RegCod=00 AND PerAno={anio} AND PerMes={mes}'
        query = ' '.join((SELECT, FROM, WHERE))
        return pd.read_sql(query, self.__conexion)

    def IPC_NC(self, anio: int, mes: int) -> float:
        DF_PONDERACIONES = self.PONDERACIONES_DIV["DivPon"]
        df_indices = self.carga_DivInd(anio, mes)['DivInd']
        return np.average(a=df_indices, weights=DF_PONDERACIONES)

    def inflacion_mensual(self, anio: int, mes: int) -> float:
        if mes == 1:
            actual = self.IPC_NC(anio, mes)
            anterior = self.IPC_NC(anio - 1, 12)
        else:
            actual = self.IPC_NC(anio, mes)
            anterior = self.IPC_NC(anio, mes - 1)
        return 100*(actual/anterior - 1)

    def inflacion_interanual(self, anio: int, mes: int) -> float:
        actual = self.IPC_NC(anio, mes)
        anterior = self.IPC_NC(anio - 1, mes)
        return 100*(actual/anterior - 1)

p = sql_INE()
print(p.inflacion_interanual(2022, 8))