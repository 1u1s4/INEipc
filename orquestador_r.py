# prueba usar R en py
import os
os.environ["R_HOME"] = r"C:\Program Files\R\R-4.2.1" # change as needed
import rpy2.robjects.packages as rpackages

devtools = rpackages.importr('devtools')
#devtools.install_github("1u1s4/funcionesINE")
