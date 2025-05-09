import pkg_resources
import configparser
from getpass import getpass
import warnings
from typing import List, Tuple

warnings.filterwarnings("ignore")
import os

import numpy as np
import pandas as pd
import datetime

from utilsjo import mes_by_ordinal, r0und
from INEcodex import Codex
from INEfnts import Fuentes

class SqlIPC:
    def __init__(
        self, anio: int, mes: int, dbBackup: bool=False, dbPack: bool=False
    ) -> None:
        # cargar Codex
        self.__codex = Codex()
        self.__codex.cargar_clave()
        self.anio = anio
        self.mes = mes
        # diccionario tipo de fuentes
        self.nombre_fuentes = {
            352271: 'Tiendas grandes',
            352272: 'Tiendas no especializadas',
            352274: 'Mercados',
            352275: 'Puestos callejeros',
            352277: 'Servicios especializados',
            352278: 'Servicios básicos y regulados',
            352279: 'Tiendas o almacenes',
            352280: 'Servicios individuales',
            352281: 'Plataformas digitales',
        }
        if dbBackup:
            self.df_DivInd = self.__codex.cargar_df('db_b/df_DivInd.parquet')
            self.df_DivPon = self.__codex.cargar_df('db_b/df_DivPon.parquet')
            self.df_GbaInd = self.__codex.cargar_df('db_b/df_GbaInd.parquet')
            self.df_GbaPon = self.__codex.cargar_df('db_b/df_GbaPon.parquet')
            self.df_GbaInfo = self.__codex.cargar_df('db_b/df_GbaInfo.parquet')
            self.df_DivNom = self.__codex.cargar_df('db_b/df_DivNom.parquet')
            self.df_Fnt = self.__codex.cargar_df('db_b/df_Fnt.parquet')
        elif dbPack:
            self.df_DivInd = self.__codex.cargar_df(
                pkg_resources.resource_filename(
                    __name__, 'db_pack/df_DivInd.parquet'
                )
            )
            self.df_DivPon = self.__codex.cargar_df(
                pkg_resources.resource_filename(
                    __name__, 'db_pack/df_DivPon.parquet'
                )
            )
            self.df_GbaInd = self.__codex.cargar_df(
                pkg_resources.resource_filename(
                    __name__, 'db_pack/df_GbaInd.parquet'
                )
            )
            self.df_GbaPon = self.__codex.cargar_df(
                pkg_resources.resource_filename(
                    __name__, 'db_pack/df_GbaPon.parquet'
                )
            )
            self.df_GbaInfo = self.__codex.cargar_df(
                pkg_resources.resource_filename(
                    __name__, 'db_pack/df_GbaInfo.parquet'
                )
            )
            self.df_DivNom = self.__codex.cargar_df(
                pkg_resources.resource_filename(
                    __name__, 'db_pack/df_DivNom.parquet'
                )
            )
            self.df_Fnt = self.__codex.cargar_df(
                pkg_resources.resource_filename(
                    __name__, 'db_pack/df_Fnt.parquet'
                )
            )
        else:
            # datos servidor
            if os.path.exists('config.ini'):
                config = configparser.ConfigParser()
                config.read('config.ini')
                db_config = config['prod']
                SERVER = db_config['SERVER']
                DATABASE = db_config['DATABASE']
                USERNAME = db_config['USERNAME']
                PASSWORD = db_config['PASSWORD']
            elif all([
                    os.getenv('SERVER'),
                    os.getenv('DATABASE'),
                    os.getenv('USERNAME'),
                    os.getenv('PASSWORD')
                ]):
                SERVER = os.getenv('SERVER')
                DATABASE = os.getenv('DATABASE')
                USERNAME = os.getenv('USERNAME')
                PASSWORD = os.getenv('PASSWORD')
            else:
                print(
                    'Datos de conexión no encontrados. '
                    'Ingrese los datos de conexión a la base de datos:'
                )
                os.environ['SERVER'] = input('Servidor: ')
                os.environ['DATABASE'] = input('Base de datos: ')
                os.environ['USERNAME'] = input('Usuario: ')
                os.environ['PASSWORD'] = input('Contraseña: ')
                SERVER = os.getenv('SERVER')
                DATABASE = os.getenv('DATABASE')
                USERNAME = os.getenv('USERNAME')
                PASSWORD = os.getenv('PASSWORD')
            # conexion
            import pyodbc
            self.__conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}'
                + f';SERVER={SERVER};DATABASE={DATABASE}'
                + f';UID={USERNAME};PWD={PASSWORD}'
            )
            self.Grupos = pd.DataFrame() 
            """ Temporary
            for j in range(2023,anio):
                for i in range(1,13):
                    temp_df = pd.read_sql(
                        f'EXEC sp_get_indice_grupo {j}, {i}',
                        self.__conexion
                    )
                    temp_df['PerAno'] = j
                    temp_df['PerMes'] = i
                    self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)
            for i in range(1, mes+1):
                temp_df = pd.read_sql(
                    f'EXEC sp_get_indice_grupo {anio}, {i}',
                    self.__conexion
                )
                temp_df['PerAno'] = anio
                temp_df['PerMes'] = i
                self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)
            """
            temp_df = pd.read_sql(
                f'EXEC sp_get_indice_grupo 2024, 12',
                self.__conexion
            )
            temp_df['PerAno'] = 2024
            temp_df['PerMes'] = 12
            self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)
            temp_df = pd.read_sql(
                f'EXEC sp_get_indice_grupo 2025, 1',
                self.__conexion
            )
            temp_df['PerAno'] = 2025
            temp_df['PerMes'] = 1
            self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)
            temp_df = pd.read_sql(
                f'EXEC sp_get_indice_grupo 2025, 2',
                self.__conexion
            )
            temp_df['PerAno'] = 2025
            temp_df['PerMes'] = 2
            self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)
            temp_df = pd.read_sql(
                f'EXEC sp_get_indice_grupo 2025, 3',
                self.__conexion
            )
            temp_df['PerAno'] = 2025
            temp_df['PerMes'] = 3
            self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)

            temp_df = pd.read_sql(
                f'EXEC sp_get_indice_grupo 2025, 4',
                self.__conexion
            )
            temp_df['PerAno'] = 2025
            temp_df['PerMes'] = 4
            self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)

            #temp_df = pd.read_excel("Índices_good.xlsx")
            #temp_df['PerAno'] = 2024
            #temp_df['PerMes'] = 1
            #self.Grupos = pd.concat([self.Grupos,temp_df], ignore_index=True)
            # Nombres de las divisiones
            self.df_DivNom = self.Grupos[
                self.Grupos['tipo_grupo'] == 'División'
            ].rename(
                columns={
                    'grupo_codigo': 'DivCod',
                    'grupo_nombre': 'DivNom'
                }
            )[['DivCod', 'DivNom']].head(13)
            # ponderaciones de las divisiones
            self.df_DivPon = self.Grupos[
                self.Grupos['tipo_grupo'] == 'División'
            ].rename(
                columns={
                    'region_id':            'RegCod',
                    'grupo_codigo':         'DivCod',
                    'ponderacion_region':   'DivPon',
                }
            )[['RegCod', 'DivCod', 'DivPon']].head(13 * 9)
            self.df_DivPon = self.df_DivPon.astype({
                'RegCod': 'int64', 'DivCod': 'int64'
            })
            # ponderaciones de los productos
            self.df_GbaPon = self.Grupos[
                self.Grupos['tipo_grupo'] == 'Producto'
            ]
            self.df_GbaPon = self.df_GbaPon[
                self.df_GbaPon['PerAno'] == self.anio
            ]
            self.df_GbaPon = self.df_GbaPon[
                self.df_GbaPon['PerMes'] == self.mes
            ]
            self.df_GbaPon = self.df_GbaPon.rename(
                columns={
                    'region_id':            'RegCod',
                    'grupo_codigo':         'GbaCod',
                    'ponderacion_region':   'GbaPon',
                }
            )[['RegCod', 'GbaCod', 'GbaPon']]
            self.df_GbaPon.insert(
                1, 'DivCod', self.df_GbaPon['GbaCod'] // 1_0_0_0_00_00
            )
            columnas = ("RegCod", "DivCod", "GbaCod")
            self.df_GbaPon = self.df_GbaPon.astype(
                dict.fromkeys(columnas, "int64")
            )
            # informacion productos
            self.df_GbaInfo = self.Grupos[
                self.Grupos['tipo_grupo'] == 'Producto'
            ]
            self.df_GbaInfo = self.df_GbaInfo[
                self.df_GbaInfo['PerAno'] == self.anio
            ]
            self.df_GbaInfo = self.df_GbaInfo[
                self.df_GbaInfo['PerMes'] == self.mes
            ]
            self.df_GbaInfo = self.df_GbaInfo.rename(
                columns={
                    'grupo_codigo': 'GbaCod',
                    'grupo_nombre': 'GbaNom'
                }
            )
            self.df_GbaInfo = self.df_GbaInfo[
                self.df_GbaInfo['region_id'] == 0
            ][['GbaCod', 'GbaNom']]
            self.df_GbaInfo.insert(0, 'SubCod', self.df_GbaInfo['GbaCod'] // 100)
            self.df_GbaInfo.insert(0, 'GruCod', self.df_GbaInfo['SubCod'] // 10)
            self.df_GbaInfo.insert(0, 'AgrCod', self.df_GbaInfo['GruCod'] // 10)
            self.df_GbaInfo.insert(0, 'DivCod', self.df_GbaInfo['AgrCod'] // 10)
            columnas = ('DivCod', 'AgrCod', 'GruCod', 'SubCod', 'GbaCod')
            self.df_GbaInfo = self.df_GbaInfo.astype(dict.fromkeys(columnas, "int64"))
            # indices por division
            self.df_DivInd = self.Grupos[self.Grupos['tipo_grupo'] == 'División'].rename(
                columns={
                    'region_id':    'RegCod',
                    'grupo_codigo': 'DivCod',
            #        'codigo': 'DivCod',
                    'indice_grupo': 'DivInd'
                }
            )[['RegCod', 'PerAno', 'PerMes', 'DivCod', 'DivInd']]
            self.df_DivInd = self.df_DivInd.astype({"RegCod": "int64", "DivCod": "int64"})

            # indices por gasto basico
            self.df_GbaInd = self.Grupos[self.Grupos['tipo_grupo'] == 'Producto'].rename(
                columns={
                    'region_id':    'RegCod',
                    'grupo_codigo': 'GbaCod',
            #        'codigo': 'GbaCod',
                    'indice_grupo': 'GbaInd'
                }
            )[['RegCod', 'PerAno', 'PerMes', 'GbaCod', 'GbaInd']]
            self.df_GbaInd.insert(3, 'SubCod', self.df_GbaInd['GbaCod'] // 100)
            self.df_GbaInd.insert(3, 'GruCod', self.df_GbaInd['SubCod'] // 10)
            self.df_GbaInd.insert(3, 'AgrCod', self.df_GbaInd['GruCod'] // 10)
            self.df_GbaInd.insert(3, 'DivCod', self.df_GbaInd['AgrCod'] // 10)
            columnas = ('RegCod', 'PerAno', 'PerMes', 'DivCod', 'AgrCod', 'GruCod', 'SubCod', 'GbaCod')
            for columna in columnas:
                self.df_GbaInd[columna] = self.df_GbaInd[columna].astype('int64')
            self.df_GbaInd = self.df_GbaInd[self.df_GbaInd['PerAno'] >= self.anio - 2]
            # extractor de boletas
            fuentes = Fuentes(self.__conexion)
            self.df_Fnt = fuentes.boletas_ultimos_12_meses(self.anio, self.mes)
            # Comprobamos si la carpeta db_b existe
            if not os.path.exists("db_b"):
                # Si no existe, la creamos
                os.makedirs("db_b")
            # Guardar los dataframes en la carpeta "db_b"
            self.__codex.guardar_df(self.df_DivInd, 'db_b/df_DivInd.parquet')
            self.__codex.guardar_df(self.df_DivPon, 'db_b/df_DivPon.parquet')
            self.__codex.guardar_df(self.df_GbaInd, 'db_b/df_GbaInd.parquet')
            self.__codex.guardar_df(self.df_GbaPon, 'db_b/df_GbaPon.parquet')
            self.__codex.guardar_df(self.df_GbaInfo, 'db_b/df_GbaInfo.parquet')
            self.__codex.guardar_df(self.df_DivNom, 'db_b/df_DivNom.parquet')
            self.__codex.guardar_df(self.df_Fnt, 'db_b/df_Fnt.parquet')
            # Obtener la marca temporal actual
            now = datetime.datetime.now()
            # Crear el nombre del archivo con la marca temporal
            # Crear el archivo en la carpeta "db_b" con la marca temporal como nombre
            with open('db_b/marca_temporal.txt', 'w') as file:
                file.write('Backup creado el ' + now.strftime("%d-%m-%Y %H:%M"))
        
        # Empalmes
        self.empalmes = pd.read_excel('Empalme IPC 23 01 2023.xlsx', sheet_name='Regiones')
        
        # Empalmes
        EmpalmeR0Div = pd.read_excel("Empalmes_2024_Div.xlsx")
        for idx, row in self.df_DivInd.iterrows():
            if row["PerAno"] == 2024 and row["RegCod"] == 0:
                self.df_DivInd.at[idx, "DivInd"] = EmpalmeR0Div.iloc[int(row["PerMes"]) - 1, int(row["DivCod"])]
        

        # Empalmes
        self.empalmes_2024_gba = pd.read_excel('Empalmes_prod_2024.xlsx')
            
        # fin de carga de datos 
        # nombre de divisiones
        abr_diviciones = {
            'Alimentos Y Bebidas No Alcohólicas':                               'Alimentos',
            'Bebidas Alcohólicas, Tabaco Y Narcóticos':                         'Bebidas Alcohólicas',
            'Vestuario Y Calzado':                                              'Vestuario',
            'Vivienda, Agua, Electricidad, Gas Y Otros Combustibles':           'Vivienda',
            'Mobiliario, Equipo Y Mantenimiento Rutinario Del Hogar':           'Muebles',
            'Salud':                                                            'Salud',
            'Transporte':                                                       'Transporte',
            'Información Y Comunicación':                                       'Comunicaciones',
            'Recreación, Deporte Y Cultura':                                    'Recreación',
            'Servicios Educativos':                                             'Educación',
            'Restaurantes Y Servicios De Alojamiento':                          'Restaurantes',
            'Cuidado Personal, Protección Social, Bienes Y Servicios Diversos': 'Bienes diversos',
            'Seguros Y Servicios Financieros':                                  'Seguros'
        }
        df_DivNom_dic = self.df_DivNom.to_dict()
        self.NOMBRE_DIV = dict(zip(
            [int(i) for i in df_DivNom_dic['DivCod'].values()],
            [abr_diviciones[nombre.strip().title()] for nombre in df_DivNom_dic['DivNom'].values()]
        ))

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
        
        if anio == 2024:
            if mes == 1:
                return [
                    98.8566959789581,
                    99.0703516980739,
                    98.4589459109483,
                    99.2732399599357,
                    98.7060730128276,
                    98.9889558644043,
                    99.0633198918171,
                    98.3610164417958,
                    99.0030424784213
                ][RegCod]
            elif mes == 2:
                return [
                    98.9946170444611,
                    99.4364034366602,
                    98.4472428743909,
                    99.3516937093573,
                    99.1422555329436,
                    98.9869047727995,
                    99.0687058323882,
                    98.4382783462334,
                    99.0913595283268
                ][RegCod]
            elif mes == 3:
                return [
                    99.3001063784863,
                    100.0180590542190,
                    98.4599639511934,
                    99.5920528652636,
                    99.4853949248333,
                    99.3307836871359,
                    99.3552364851949,
                    98.5871297222272,
                    99.3728206059840
                ][RegCod]
            elif mes == 4:
                return [
                    99.5941332154716,
                    100.3758691360640,
                    98.7136763017206,
                    100.1194001167880,
                    99.8160867445613,
                    99.5781514691463,
                    99.5287613558820,
                    98.8357987784852,
                    99.5104659063637
                ][RegCod]
            elif mes == 5:
                return [
                    99.6225049933957,
                    99.8971263223512,
                    99.0171588693267,
                    100.1115466201590,
                    99.9728445595770,
                    99.4194255169563,
                    99.6305819927960,
                    99.1436070044165,
                    99.7106211181326
                ][RegCod]
            elif mes == 6:
                return [
                    99.7815546988695,
                    99.8560061419072,
                    99.4858072043359,
                    100.2289957443490,
                    99.9760410152592,
                    99.5714757744731,
                    99.8301582735396,
                    99.5040948972420,
                    99.7758349414034
                ][RegCod]
            elif mes == 7:
                return [
                    100.6382598378680,
                    100.3104705403120,
                    100.8659796107090,
                    100.5939105012150,
                    100.5739172998620,
                    100.5797124613060,
                    100.8777504364930,
                    101.0315533218260,
                    100.4038266822690
                ][RegCod]
            elif mes == 8:
                return [
                    100.5755433856820,
                    100.3203383436650,
                    100.8337411583420,
                    100.5213375634430,
                    100.5550741866870,
                    100.4156993780340,
                    100.8389200643260,
                    100.7556405465690,
                    100.4397388714060
                ][RegCod]
            elif mes == 9:
                return [
                    100.1963145064570,
                    100.0635322555170,
                    100.3741125085020,
                    100.0828885147640,
                    100.3514075127210,
                    100.1088202473040,
                    100.3420118268560,
                    100.2302318551780,
                    100.0413903730920
                ][RegCod]
            elif mes == 10:
                return [
                    100.5259968606100,
                    100.3810654448450,
                    100.5533019453350,
                    100.0354939413890,
                    100.4958947413020,
                    100.6534990890160,
                    100.3420118268560,
                    101.1151212285570,
                    100.5812006099110
                ][RegCod]
            elif mes == 11:
                return [
                    100.3556018441820,
                    100.1687583508100,
                    100.5699964189440,
                    99.8177022757379,
                    100.2291771596140,
                    100.4689604736330,
                    100.2442733162820,
                    100.7876185586310,
                    100.5234035391140
                ][RegCod]

        if anio <= 2023:
            row = 12 * (anio - 2011) + mes - 4
            col = 6 * RegCod + 5
            return self.empalmes.iloc[row, col]
        
        """
        Calcula el índice de precios al consumidor (IPC) para una región y
        período de tiempo dados.

        Parameters
        ----------
        anio : int
            Año para el cual se desea calcular el IPC.
        mes : int
            Mes (número entero entre 1 y 12) para el cual se desea calcular el
            IPC.
        RegCod : int
            Código de la región para la cual se desea calcular el IPC.

        Returns
        -------
        float
            IPC calculado para la región y período de tiempo dados.
        """
        PONDERACIONES_REG = self.df_DivPon[
            self.df_DivPon['RegCod'] == RegCod
        ]['DivPon']
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
        """
        Calcula la inflación interanual para una región específica.
        
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
            El valor de la inflación interanual para la región y el periodo especificados, expresado como un porcentaje.
        """
        actual = self.calcular_IPC(anio, mes, RegCod)
        anterior = self.calcular_IPC(anio - 1, mes, RegCod)
        return 100*(actual/anterior - 1)
    
    def inflacion_acumulada(self, anio: int, mes: int, RegCod: int) -> float:
        """
        Calcula la inflación acumulada para una región específica.
        
        Parameters
        ----------
        anio : int
            El año para el cual se desea calcular la inflación acumulada.
        mes : int
            El mes para el cual se desea calcular la inflación acumulada, en formato numérico (1-12).
        RegCod : int
            El código de la región para la cual se desea calcular la inflación acumulada.
        
        Returns
        -------
        float
            El valor de la inflación acumulada para la región y el periodo especificados, expresado como un porcentaje.
        """
        actual = self.calcular_IPC(anio, mes, RegCod)
        anterior = self.calcular_IPC(anio - 1, 12, RegCod)
        return 100*(actual/anterior - 1)
    
    def poder_adquisitivo(self, anio: int, mes: int, RegCod: int) -> float:
        """
        Calcula el poder adquisitivo de la moneda para una región específica.
        
        Parameters
        ----------
        anio : int
            El año para el cual se desea calcular el poder adquisitivo.
        mes : int
            El mes para el cual se desea calcular el poder adquisitivo, en formato numérico (1-12).
        RegCod : int
            El código de la región para la cual se desea calcular el poder adquisitivo.
        
        Returns
        -------
        float
            El valor del poder adquisitivo de la moneda para la región y el periodo especificados, expresado como un porcentaje.
        """
        return (1 / self.calcular_IPC(anio, mes, RegCod)) * 100

    def incidencia_divisiones(self, RegCod: int) -> List[float]:
        """
        Calcula la incidencia de cada división en el índice de precios al consumidor
        en una determinada región y periodo.

        Args:
            RegCod (int): Código de la región.

        Returns:
            List[float]: Lista de tuplas que contiene la incidencia de cada
            división en el índice de precios al consumidor de la región, en
            orden descendente. Cada tupla contiene la variación ponderada de la
            división y su nombre.
        """
        incidencias = []
        for DivCod in range(1, 14):
            ponderacion = self.df_DivPon[
                (self.df_DivPon['RegCod'] == RegCod) &
                (self.df_DivPon['DivCod'] == DivCod)
            ]['DivPon'].iloc[0]
            Qanio = self.df_DivInd['PerAno'] == self.anio
            Qmes = self.df_DivInd['PerMes'] == self.mes
            Qreg = self.df_DivInd['RegCod'] == RegCod
            Qdiv = self.df_DivInd['DivCod'] == DivCod
            indice_actual = self.df_DivInd[
                Qanio & Qmes & Qreg & Qdiv
            ]['DivInd'].iloc[0]
            if self.mes == 1:
                Qanio = self.df_DivInd['PerAno'] == self.anio - 1
                Qmes = self.df_DivInd['PerMes'] == 12
                ipc_anterior = self.calcular_IPC(self.anio - 1, 12, RegCod)
            else:
                Qmes = self.df_DivInd['PerMes'] == self.mes - 1
                ipc_anterior = self.calcular_IPC(
                    self.anio, self.mes - 1, RegCod
                )
            indice_anterior = self.df_DivInd[
                Qanio & Qmes & Qreg & Qdiv
            ]['DivInd'].iloc[0]
            variacion = (indice_actual - indice_anterior) * ponderacion \
                / ipc_anterior
            incidencias.append((variacion, self.NOMBRE_DIV[DivCod]))
        return incidencias


    def variacion_divisiones(self, RegCod: int) -> List[float]:
        """
        Calcula la variación de cada división en el índice de precios al
        consumidor en una determinada región y periodo.

        Args:
            RegCod (int): Código de la región.

        Returns:
            List[float]: Lista de tuplas que contiene la incidencia de cada
            división en el índice de precios al consumidor de la región, en
            orden descendente. Cada tupla contiene la variación ponderada de la
            división y su nombre.
        """
        variaciones = []
        for DivCod in range(1, 14):
            Qanio = self.df_DivInd['PerAno'] == self.anio
            Qmes = self.df_DivInd['PerMes'] == self.mes
            Qreg = self.df_DivInd['RegCod'] == RegCod
            Qdiv = self.df_DivInd['DivCod'] == DivCod
            indice_actual = self.df_DivInd[
                Qanio & Qmes & Qreg & Qdiv
            ]['DivInd'].iloc[0]
            if self.mes == 1:
                Qanio = self.df_DivInd['PerAno'] == self.anio - 1
                Qmes = self.df_DivInd['PerMes'] == 12
                ipc_anterior = self.calcular_IPC(self.anio - 1, 12, RegCod)
            else:
                Qmes = self.df_DivInd['PerMes'] == self.mes - 1
                ipc_anterior = self.calcular_IPC(
                    self.anio, self.mes - 1, RegCod
                )
            indice_anterior = self.df_DivInd[
                Qanio & Qmes & Qreg & Qdiv
            ]['DivInd'].iloc[0]
            variaciones.append((
                (indice_actual / indice_anterior) * 100 - 100,
                self.NOMBRE_DIV[DivCod]
            ))
        return variaciones






    def incidencia_gasto_basico(self, RegCod: int) -> List[Tuple[float, str]]:
        """
        Obtiene la incidencia de la variación de los gastos básicos para una
        región.

        Parámetros:
        -----------
        - RegCod: int. Código de la región de interés.

        Retorna:
        --------
        - List[Tuple[float, str]]: Lista de tuplas que contienen la incidencia
        de la variación de los gastos básicos y su nombre correspondiente para
        la región de interés.
        """

        incidencias = []
        for GbaCod in self.df_GbaInfo['GbaCod'].to_list():
            ponderacion = self.df_GbaPon[
                (self.df_GbaPon['RegCod'] == RegCod) &
                (self.df_GbaPon['GbaCod'] == GbaCod)
            ]['GbaPon'].iloc[0]
            Qanio = self.df_GbaInd['PerAno'] == self.anio
            Qmes = self.df_GbaInd['PerMes'] == self.mes
            Qreg = self.df_GbaInd['RegCod'] == RegCod
            Qgba = self.df_GbaInd['GbaCod'] == GbaCod
            try:
                indice_actual = self.df_GbaInd[
                    Qanio & Qmes & Qreg & Qgba
                ]['GbaInd'].iloc[0]
            except:
                pass
            if self.mes == 1:
                Qanio = self.df_GbaInd['PerAno'] == self.anio - 1
                Qmes = self.df_GbaInd['PerMes'] == 12
                ipc_ant = self.calcular_IPC(self.anio - 1, 12, RegCod)
            else:
                Qmes = self.df_GbaInd['PerMes'] == self.mes - 1
                ipc_ant = self.calcular_IPC(self.anio, self.mes - 1, RegCod)
            try:
                indice_ant = self.df_GbaInd[
                    Qanio & Qmes & Qreg & Qgba
                ]['GbaInd'].iloc[0]
            except:
                pass
            variacion = ((indice_actual - indice_ant) / ipc_ant) * ponderacion
            nombre_gba = self.get_nombre_Gba(GbaCod)
            incidencias.append((variacion, nombre_gba))
        return incidencias

    def series_historicas_Gbas(self, RegCod: int) -> \
        List[Tuple[str, List[Tuple[str, float]]]]:

        resultado = []
        for producto, group in self.empalmes_2024_gba.groupby(by="grupo_codigo"):
            lista_meses_precios = list(zip(group['mes'], group['indice_empalmado']))
            resultado.append((producto, lista_meses_precios))
        resultado_modificable = [list(item) for item in resultado]
        ind = 0
        for gba in resultado_modificable:
            gba[0] = self.empalmes_2024_gba.iloc[ind*13,2]
            ind += 1
        return [tuple(item) for item in resultado_modificable]

        """
        Devuelve una lista de tuplas, cada una representando una serie histórica
        de un gasto básico diferente. La tupla contiene el nombre del gasto básico
        y una lista de tuplas que contienen la fecha en formato "mes-año" y el
        índice correspondiente a ese mes y año.

        Parámetros:
        -----------
        RegCod: int
            Código de región.

        Returns:
        --------
        series: List[Tuple[str, List[Tuple[str, float]]]]
            Lista de tuplas que contienen el nombre del gasto básico y la lista de
            tuplas de fecha-índice correspondientes a ese gasto básico.
        """
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
                indices1 = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba][['PerAno','PerMes','GbaInd']]
                Qanio = self.df_GbaInd['PerAno'] == self.anio - 1
                Qmes = self.df_GbaInd['PerMes'] >= self.mes
                indices2 = self.df_GbaInd[Qanio & Qmes & Qreg & Qgba][['PerAno','PerMes','GbaInd']]
                indices = pd.merge(indices2, indices1, how='outer')
            nombre_gba = self.get_nombre_Gba(GbaCod)
            indices_final = []
            indices = indices.sort_values(by=['PerAno', 'PerMes'])
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
        """
        Retorna una serie histórica del IPC para una región específica.

        Args:
            RegCod (int): Código de la región para la cual se quiere obtener la
            serie histórica del IPC.
            Qpdr_adq (bool, optional): Indica si se quiere calcular la serie
            histórica en términos de poder adquisitivo o no. Por defecto es False.

        Returns:
            List[Tuple[str, float]]: Lista de tuplas, donde cada tupla contiene
            dos elementos: la fecha en formato "mes-año" y el valor del IPC
            correspondiente a esa fecha.
        """
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
            mes_abr = mes_by_ordinal(self.mes)
            fecha = f'{mes_abr}-{self.anio - 1}'
            ipc = funcion(self.anio - 1, self.mes, RegCod)
            serie.append((fecha, ipc))
            for i in range(1, 13):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                ipc = funcion(self.anio, i, RegCod)
                serie.append((fecha, ipc))
        return serie

    def serie_historica_inflacion(self, RegCod: int, tipo: str) -> List[Tuple[str, float]]:
        """
        Retorna una serie histórica de inflación para una región específica.

        Args:
            RegCod (int): Código de la región para la cual se quiere obtener la
            serie histórica de inflación.
            tipo (str): Tipo de inflación que se desea calcular. Puede ser
            'intermensual', 'interanual' o 'acumulada'.

        Returns:
            List[Tuple[str, float]]: Lista de tuplas, donde cada tupla contiene
            dos elementos: la fecha en formato "mes-año" y el valor del índice
            de inflación correspondiente a esa fecha.
        """
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
                mes_abr = mes_by_ordinal(self.mes)
                fecha = f'{mes_abr}-{self.anio - 1}'
                indice = funcion(self.anio - 1, self.mes, RegCod)
                serie.append((fecha, indice))
                for i in range(1, 13):
                    mes_abr = mes_by_ordinal(i)
                    fecha = f'{mes_abr}-{self.anio}'
                    indice = funcion(self.anio, i, RegCod)
                    serie.append((fecha, indice))
        return serie

    def serie_fuentes_precios(self, Qfuentes: bool = True, RegCod: int = 0) -> List[Tuple[str, int]]:
        """
        Devuelve una serie histórica con la cantidad de fuentes de precios disponibles
        para cada mes y año.
        
        Parameters
        ----------
        Qfuentes : bool, optional
            Si es True, se contabilizan solamente las fuentes de precios únicas (eliminando duplicados), 
            de lo contrario, se cuentan todas las observaciones. Por defecto es True.
            
        Returns
        -------
        List[Tuple[str, int]]
            Lista de tuplas con la información de la serie histórica. 
            Cada tupla contiene dos elementos: 
            - un string con la fecha en formato 'Abr-Año'
            - un entero con la cantidad de fuentes de precios disponibles para esa fecha.
        """
        serie = []
        if self.mes != 12:
            #for i in range(self.mes, 13):
            for i in range(12, 13):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio - 1}'
                mes_ = self.df_Fnt['PerMes'] == i
                anio_ = self.df_Fnt['PerAno'] == self.anio - 1
                conteo = self.df_Fnt[anio_ & mes_]
                if RegCod != 0:
                    conteo = conteo[conteo['RegCod'] == RegCod]
                if Qfuentes:
                    conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
                serie.append((fecha, conteo.shape[0]))
            for i in range(1, self.mes + 1):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = self.df_Fnt['PerMes'] == i
                anio_ = self.df_Fnt['PerAno'] == self.anio
                conteo = self.df_Fnt[anio_ & mes_]
                if RegCod != 0:
                    conteo = conteo[conteo['RegCod'] == RegCod]
                if Qfuentes:
                    conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
                serie.append((fecha, conteo.shape[0]))
        else:
            mes_abr = mes_by_ordinal(self.mes)
            fecha = f'{mes_abr}-{self.anio - 1}'
            mes_ = self.df_Fnt['PerMes'] == self.mes
            anio_ = self.df_Fnt['PerAno'] == self.anio - 1
            conteo = self.df_Fnt[anio_ & mes_]
            if RegCod != 0:
                conteo = conteo[conteo['RegCod'] == RegCod]
            if Qfuentes:
                conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
            serie.append((fecha, conteo.shape[0]))
            for i in range(1, 13):
                mes_abr = mes_by_ordinal(i)
                fecha = f'{mes_abr}-{self.anio}'
                mes_ = self.df_Fnt['PerMes'] == i
                anio_ = self.df_Fnt['PerAno'] == self.anio
                conteo = self.df_Fnt[anio_ & mes_]
                if RegCod != 0:
                    conteo = conteo[conteo['RegCod'] == RegCod]
                if Qfuentes:
                    conteo = conteo.drop_duplicates(subset=["DepCod", "MunCod", "FntCod"])
                serie.append((fecha, conteo.shape[0]))
        return serie

    def desagregacion_fuentes(self) -> List[Tuple[str, int]]:
        """
        Desagrega el número de fuentes por tipo de fuente.

        Returns:
        -----------
        List[Tuple[str, int]]:
            Una lista de tuplas que contienen el nombre del tipo de fuente y el número de fuentes para el mes y año actual.
        """
        serie = []
        mes_ = self.df_Fnt['PerMes'] == self.mes
        anio_ = self.df_Fnt['PerAno'] == self.anio
        S = 1
        TfnCods = {
#            351841, 351842, 351843, 351844, 351845, 351846, 351847, 351848,
#            351849, 351850, 351851, 351852, 351853, 351854, 351855, 351856,
#            351857, 351858, 351859, 351860, 351861,
#            351940, 351941, 351942, 351943, 351944, 351945, 351946, 351947,
#            351948, 351949,

#            352271, 352272, 352273, 352274, 352275, 352276, 352277, 352278,
#            352279, 352280, 352281

            352271, 352272, 352274, 352275, 352277, 352278, 352279,
            352280, 352281
        }
        for i in TfnCods:
            tipo_fuente_ = self.df_Fnt['TfnCod'] == i
            conteo = self.df_Fnt[anio_ & mes_ & tipo_fuente_].drop_duplicates(subset=["DepCod", "MunCod", "FntCod"]).shape[0]
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
    
    def desagregacion_fuentes_cantidad(self) -> List[Tuple[str, int]]:
        """
        Desagrega el número de fuentes por tipo de fuente.

        Returns:
        -----------
        List[Tuple[str, int]]:
            Una lista de tuplas que contienen el nombre del tipo de fuente y el número de fuentes para el mes y año actual.
        """
        serie = []
        mes_ = self.df_Fnt['PerMes'] == self.mes
        anio_ = self.df_Fnt['PerAno'] == self.anio
        S = 1
        TfnCods = {
#            351841, 351842, 351843, 351844, 351845, 351846, 351847, 351848,
#            351849, 351850, 351851, 351852, 351853, 351854, 351855, 351856,
#            351857, 351858, 351859, 351860, 351861,
#            351940, 351941, 351942, 351943, 351944, 351945, 351946, 351947,
#            351948, 351949,

#            352271, 352272, 352273, 352274, 352275, 352276, 352277, 352278,
#            352279, 352280, 352281

            352271, 352272, 352274, 352275, 352277, 352278, 352279,
            352280, 352281
        }
        for i in TfnCods:
            tipo_fuente_ = self.df_Fnt['TfnCod'] == i
            conteo = self.df_Fnt[anio_ & mes_ & tipo_fuente_].drop_duplicates(subset=["DepCod", "MunCod", "FntCod"]).shape[0]
            S += conteo
            nmbr_Fnt = self.nombre_fuentes.get(i)
            serie.append((nmbr_Fnt, conteo))
        invertir = [(i[1] , i[0]) for i in serie]
        serie = [i[::-1] for i in sorted(invertir, reverse=True)]
        # hacer pareto
        acumulado = 0
        for i, fuente in enumerate(serie):
            acumulado += fuente[1]
            if acumulado >= 80:
                break
        return serie

    def cobertura_fuentes_precios(self, Qfuentes: bool = True) -> List[Tuple[int, int]]:
        """Calcula la cobertura de fuentes de precios para cada región en un mes
        y año específico.

        Args:
            Qfuentes (bool, optional): Si se requiere el conteo de fuentes
            únicas. Defaults to True.

        Returns:
            List[Tuple[int, int]]: Una lista de tuplas que contiene el código de
            región y el número de fuentes de precios para la región especificada
            en el mes y año específico.
        """
        cobertura = []
        mes_ = self.df_Fnt['PerMes'] == self.mes
        anio_ = self.df_Fnt['PerAno'] == self.anio
        for i in range(1, 9):
            RegCod_ = self.df_Fnt['RegCod'] == i
            conteo = self.df_Fnt[anio_ & mes_ & RegCod_]
            if Qfuentes:
                conteo = conteo.drop_duplicates(
                    subset=["DepCod", "MunCod", "FntCod"]
                )
            cobertura.append((i, conteo.shape[0]))
        return cobertura

    def serie_historica(self, tipo: str) -> List[Tuple[str, float]]:
        serie = []
        if tipo == 'mensual':
            funcion = self.inflacion_mensual
        elif tipo == 'anual':
            funcion = self.inflacion_interanual
        elif tipo == 'IPC':
            funcion = self.calcular_IPC
        if tipo != 'anual':
            anio_inf = 2011
        else:
            anio_inf = 2012
        for anio in range(anio_inf, self.anio):
            mes_inf = 4 if anio == anio_inf else 1
            for mes in range(mes_inf, 13):
                indice = funcion(anio, mes, 0)
                mes_abr = mes_by_ordinal(mes)
                fecha = f'{mes_abr}-{anio}'
                serie.append((fecha, indice))
        for mes in range(1, self.mes + 1):
                indice = funcion(self.anio, mes, 0)
                mes_abr = mes_by_ordinal(mes)
                fecha = f'{mes_abr}-{self.anio}'
                serie.append((fecha, indice))
        return serie

    def serie_historica_mensual_inflacion(self, RegCod: int, tipo: str) -> List[Tuple[str, float]]:
        """
        Retorna una serie histórica de inflación para una región específica.

        Args:
            RegCod (int): Código de la región para la cual se quiere obtener la
            serie histórica de inflación.
            tipo (str): Tipo de inflación que se desea calcular. Puede ser
            'intermensual', 'interanual' o 'acumulada'.

        Returns:
            List[Tuple[str, float]]: Lista de tuplas, donde cada tupla contiene
            dos elementos: la fecha en formato "mes-año" y el valor del índice
            de inflación correspondiente a esa fecha.
        """
        serie = []
        if tipo == 'intermensual':
            funcion = self.inflacion_mensual
        elif tipo == 'interanual':
            funcion = self.inflacion_interanual
        elif tipo == 'acumulada':
            funcion = self.inflacion_acumulada

        for anio in range(2012 + (self.mes < 4), self.anio + 1):
            mes_abr = mes_by_ordinal(self.mes)
            fecha = f'{mes_abr}-{anio}'
            indice = funcion(anio, self.mes, RegCod)
            serie.append((fecha, indice))
        return serie
    
    def deteccion_Fnt_sin_tipo(self):
        mes_ = self.df_Fnt['PerMes'] == self.mes
        anio_ = self.df_Fnt['PerAno'] == self.anio
        tipo_fuente = 0

        tipo_fuente_ = self.df_Fnt['TfnCod'] == str(tipo_fuente).zfill(2)
        sin_fuente = self.df_Fnt[anio_ & mes_ & tipo_fuente_].drop_duplicates(
            subset=["DepCod", "MunCod", "FntCod"]
        )

        nmbr_Fnt = self.nombre_fuentes.get(tipo_fuente)

        return (sin_fuente, nmbr_Fnt)
