from setuptools import setup
setup(
    name='automatizacion_capitulo_1_IPC_INE',
    version='0.1',
    author='Luis Alfredo Alvarado Rodríguez',
    description='Automatizacion de extraccion de datos para el capitulo 1 del IPC.',
    long_description='',
    url='https://github.com/1u1s4/INE_IPC',
    keywords='development, setup, setuptools',
    python_requires='>=3.9',
    install_requires=[
        'fredapi',
        'xlrd=1.2.0',
        'prettytable',
        'rpy2',
        'xlsxwriter'
    ]
)