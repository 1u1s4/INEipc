""" # prueba usar R en py
import imp
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.1" # change as needed
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
devtools = rpackages.importr('devtools')
devtools.install_github("1u1s4/funcionesINE")
funcionesINE = rpackages.importr('funcionesINE')
ruta = 'C:/Users/laalvarado/Documents/pruebas/'
funcionesINE.escribirCSV(
    funcionesINE.leerLibroNormal(f'{ruta}/Libros/pobrezaCocinado.xlsx'),
    ruta=f"{ruta}CSVENCOVI/"
    ) """

from xlsxchef import xlsxChef
from funcionesjo import hoy
"""
data := {
    'nombre':str,
    'fecha_inicial': str,
    'fecha_final': str,
    'presentacion': str,
    'capitulos':[
        {
            'titulo': str,
            'resumen': str,
            'sub_capitulos':[
                {
                    'titulo': str,
                    'titulo_grafico': str,
                    'descripcion_grafico': str,
                    'descripcion': str,
                    'fuente': str,
                    'tipo_grafico': str,
                    'data: list[tuple[str, int]]
                }
            ]
        }
    ]
}
"""
class ReporteINE:
    """
    Clase para la creacion de reportes estilo INE.

    Attributes
    ----------
    nombre : str
        nombre del reporte, sera el titulo principal del documento.
    fecha_inicio : str
        
    fecha_final : str
        

    Methods
    -------
    hacer_graficas()
        
    """
    def __init__(self, nombre: str, fecha_inicial: str, fecha_final: str) -> None:
        self.__data = {}
        self.__data['nombre'] = nombre
        self.__data['fecha_inicio'] = fecha_inicial
        self.__data['fecha_final'] = fecha_final
        self.__data['capitulos'] = []

    def agregar_capitulo(self, titulo: str, resumen: str = "") -> None:
        capitulo_nuevo = {}
        capitulo_nuevo["titulo"] = titulo
        capitulo_nuevo["resumen"] = resumen
        capitulo_nuevo["sub_capitulos"] = []
        self.__data.get('capitulos').append(capitulo_nuevo)

    def agregar_subcapitulo(
        self,
        indice_capitulo: str,
        titulo: str,
        titulo_grafico: str,
        descripcion_grafico: str,
        descripcion: str,
        fuente: str,
        tipo_grafico: str,
        data: tuple
        ) -> None:
        sub_cap = {}
        sub_cap["titulo"] = titulo
        sub_cap["titulo_grafico"] = titulo_grafico
        sub_cap["descripcion_grafico"] = descripcion_grafico
        sub_cap["descripcion"] = descripcion
        sub_cap["fuente"] = fuente
        sub_cap["tipo_grafico"] = tipo_grafico
        sub_cap["data"] = data
        self.__data.get('capitulos')[indice_capitulo]['sub_capitulos'].append(sub_cap)
    
    def hacer_graficas(self) -> None:
        chef = xlsxChef()
