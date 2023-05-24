from setuptools import setup, find_packages
setup(
    name='ineipc',
    version='0.1',
    author='Luis Alfredo Alvarado Rodríguez',
    description='ETL para el informe mensual de IPC.',
    long_description='',
    url='https://github.com/1u1s4/INE_IPC',
    keywords='development, setup, setuptools',
    python_requires='>=3.9',
    packages=find_packages(),
    py_modules=['datosipc', 'descriptoripc', 'sqline'],
    install_requires=[
        'fredapi',
        'xlrd==2.0.1',
        'prettytable',
        'xlsxwriter',
        'pyodbc',
        'requests',
        'bs4',
        'numpy',
        'pandas'
    ]
)