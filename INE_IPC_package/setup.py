from setuptools import setup, find_packages
setup(
    name='datosIPC',
    version='1.0',
    author='Luis Alfredo Alvarado Rodríguez',
    description='Automatizacion de extraccion de datos para el capitulo 1 del IPC.',
    long_description='',
    url='https://github.com/1u1s4/INE_IPC',
    keywords='development, setup, setuptools',
    python_requires='>=3.9',
    packages=find_packages(),
    install_requires=[
        'fredapi',
        'xlrd==1.2.0',
        'prettytable',
        'rpy2',
        'xlsxwriter'
    ]
)