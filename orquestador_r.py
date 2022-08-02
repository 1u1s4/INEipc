# prueba usar R en py
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
    )