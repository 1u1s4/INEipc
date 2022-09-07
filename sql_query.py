import warnings
warnings.filterwarnings("ignore")
import pyodbc 
import pandas as pd

#Datos servidor
DATABASE = 'IPC2010_RN'
SERVER = '10.0.3.185'
USERNAME = 'laalvarado'
PASSWORD = 'Abc$2022'

def carga_ponderaciones() -> pd.DataFrame:
    global DATABASE, SERVER, USERNAME, PASSWORD
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}' + f';SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')
    SELECT = 'SELECT DivCod, DivPon'
    FROM = 'FROM IPCP01'
    WHERE = f'WHERE RegCod=00'
    query = ' '.join((SELECT, FROM, WHERE))
    return pd.read_sql(query, conexion)
    
def carga_DivInd(anio: int, mes: int) -> pd.DataFrame:
    global DATABASE, SERVER, USERNAME, PASSWORD
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}' + f';SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}')
    SELECT = 'SELECT DivCod, DivInd'
    FROM = 'FROM IPCPH1'
    WHERE = f'WHERE RegCod=00 AND PerAno={anio} AND PerMes={mes}'
    query = ' '.join((SELECT, FROM, WHERE))
    return pd.read_sql(query, conexion)

DF_PONDERACIONES = carga_ponderaciones()

def calculo_IPC_NC(anio: int, mes: int) -> float:
    global DF_PONDERACIONES
    df_indices = carga_DivInd(anio, mes)
    suma_indices = 0
    for i in range(0, 12):
        peso = DF_PONDERACIONES.iat[i, 1]
        indice = df_indices.iat[i, 1]
        suma_indices += peso * indice
    return round(suma_indices/100, 2)

for i in range(1, 9):
    print(i, calculo_IPC_NC(2022, i))