import imp
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.1" # change as needed
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
from xlsxchef import xlsxChef
import pathlib
from datetime import datetime
"""
data := {
    'nombre':str,
    'fecha_inicial': str,
    'fecha_final': str,
    'presentacion': str,w
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
                    'precision': int = 1,
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
    def __init__(self, nombre: str, fecha_inicial: str = "", fecha_final: str = "") -> None:
        self.__data = {}
        self.__data['nombre'] = nombre
        self.__data['fecha_inicio'] = fecha_inicial
        self.__data['fecha_final'] = fecha_final
        self.__data['capitulos'] = []
        # hacer directorio para guardar documentos
        marca_temporal = datetime.strftime(datetime.today(), "%d-%m-%Y_%H_%M_%S")
        parent_dir = pathlib.Path().resolve()
        self.__path = os.path.join(parent_dir, marca_temporal)
        os.mkdir(self.__path)
        os.mkdir(os.path.join(self.__path, "libros"))
        os.mkdir(os.path.join(self.__path, "csv"))
        os.mkdir(os.path.join(self.__path, "csv_cocinado"))
        os.mkdir(os.path.join(self.__path, "graficas"))
        # cargar modulo de R
        devtools = rpackages.importr('devtools')
        devtools.install_github("1u1s4/funcionesINE")
        self.__funcionesINE = rpackages.importr('funcionesINE')

    @property
    def data(self):
        return self.__data

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
        data: tuple,
        precision: int = 1
        ) -> None:
        sub_cap = {}
        sub_cap["titulo"] = titulo
        sub_cap["titulo_grafico"] = titulo_grafico
        sub_cap["descripcion_grafico"] = descripcion_grafico
        sub_cap["descripcion"] = descripcion
        sub_cap["fuente"] = fuente
        sub_cap["tipo_grafico"] = tipo_grafico
        sub_cap["precision"] = precision
        sub_cap["data"] = data
        self.__data.get('capitulos')[indice_capitulo]['sub_capitulos'].append(sub_cap)
    
    def escribir_libros(self) -> None:
        i = 0
        for capitulo in self.__data['capitulos']:
            i += 1
            nombre_doc = capitulo["titulo"]
            csv_chef = xlsxChef(
                tipo="csv",
                path=self.__path,
                nombre=nombre_doc,
                NoCapitulo=i
            )
            cocinado_chef = xlsxChef(
                tipo="cocinado",
                path=self.__path,
                nombre=nombre_doc,
                NoCapitulo=i
            )
            sub_capitulos = capitulo["sub_capitulos"]
            for sub_capitulo in sub_capitulos:
                if sub_capitulo["tipo_grafico"] == "lineal":
                    encabezados = True 
                    if len(sub_capitulo["data"][0]) > 2:
                        encabezados = False
                    k = sub_capitulos.index(sub_capitulo) + 1
                    csv_chef.escribir_hoja(
                        datos=sub_capitulo["data"],
                        ordinal=k,
                        encabezadosXY=encabezados
                    )
                    datos_cocinado = (
                        sub_capitulo["titulo"],
                        sub_capitulo["titulo_grafico"],
                        sub_capitulo["descripcion_grafico"],
                        sub_capitulo["descripcion"]
                    )
                    cocinado_chef.escribir_hoja(
                        datos=datos_cocinado,
                        ordinal=k
                    )
            cocinado_chef.cerrar_libro()
            csv_chef.cerrar_libro()
    
    def generar_csv(self):
        ruta = self.__path.replace("\\", "/")
        i = 0
        for capitulo in self.__data['capitulos']:
            i += 1
            nombre = capitulo['titulo'].title().replace(" ", "")
            libro_cocinado = f"{nombre}_cocinado.xlsx"
            libro_csv = f"{nombre}_csv.xlsx"
            csv_path = os.path.join(self.__path, "csv")
            os.mkdir(os.path.join(csv_path, str(i)))
            self.__funcionesINE.escribirCSV(
                self.__funcionesINE.leerLibroNormal(f'{ruta}/libros/{libro_cocinado}'),
                ruta=f"{ruta}/csv_cocinado"
                )
            self.__funcionesINE.escribirCSV(
                lista=self.__funcionesINE.leerLibro(ruta=f'{ruta}/libros/{libro_csv}'),
                ruta=f"{ruta}/csv/{i}"
                )
    
    def hacer_graficas(self):
        self.__funcionesINE.anual()
        ruta_tex = self.__path.replace("\\", "/") + "/graficas"
        i = 0
        for capitulo in self.__data['capitulos']:
            i += 1
            csv_path = os.path.join(self.__path, f"csv\\{i}").replace("\\", "/")
            datos = self.__funcionesINE.cargaMasiva(csv_path, codificacion='utf-8')
            sub_capitulos = capitulo["sub_capitulos"]
            for sub_capitulo in sub_capitulos:
                indice = sub_capitulos.index(sub_capitulo)
                if sub_capitulo["tipo_grafico"] == "lineal":
                    indice_natural = str(indice + 1).rjust(2, "0")
                    referencia = f"{i}_{indice_natural}"
                    self.__funcionesINE.cuatroEtiquetas()
                    self.__funcionesINE.exportarLatex(
                        ruta_tex + f"/{referencia}.tex",
                        self.__funcionesINE.graficaLinea(#
                            datos[indice],
                            precision=sub_capitulo["precision"]
                        )
                    )