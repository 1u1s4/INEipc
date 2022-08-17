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
    'fecha_inicial':str,
    'fecha_final':str,
    'presentacion':str,
    'capitulos':[
        {
            'titulo':str,
            'resumen':str,
            'sub_capitulos':[
                {
                    'titulo':str,
                    'titulo_grafico':str,
                    'descripcion_grafico':str,
                    'descripcion':str,
                    'fuente':str,
                    'tipo_grafico':str,
                    'data':list[tuple[str, int]]
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
    def __init__(self, nombre:str, fecha_inicial:str, fecha_final:str) -> None:
        self._data = {}
        self._data['nombre'] = nombre
        self._data['fecha_inicio'] = fecha_inicial
        self._data['fecha_final'] = fecha_final

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, new_data: dict):
        self._data.append(new_data)
    
    def hacer_graficas(self) -> None:
        pass