from setuptools import setup
setup(
    name='app-name',
    version='1.0',
    author='Bejamin Frakline',
    description='A brief synopsis of the project',
    long_description='A much longer explanation of the project and helpful resources',
    url='https://github.com/BenjaminFranline',
    keywords='development, setup, setuptools',
    python_requires='>=3.7',
    install_requires=[
        'fredapi',
        'xlrd',
        'prettytable'
    ]
)