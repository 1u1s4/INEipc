# xlsx_chef.py
import xlsxwriter
from datosipc import datosIPC

class xlsxChef:
    def __init__(self, tipo: str, path: str, nombre: str = 'XLSXprueba', NoCapitulo: int = 0) -> None:
        self.__tipo = tipo
        nombre = f"{nombre.title()}_{tipo}.xlsx".replace(" ", "")
        self.__workbook = xlsxwriter.Workbook(f"{path}\\libros\\{nombre}")
        self.__NoCapitulo = NoCapitulo

    def escribir_hoja(self, datos:tuple, ordinal: int, encabezadosXY: bool = True) -> None:
        ordinal = str(ordinal).rjust(2, "0")
        worksheet = self.__workbook.add_worksheet(f"{self.__NoCapitulo}_{ordinal}")
        if self.__tipo == "csv":
            if encabezadosXY:
                worksheet.write(0, 0, "x")
                worksheet.write(0, 1, "y")
                row = 1
            else:
                row = 0
            for fila in datos:
                col = 0
                for celda in fila:
                    worksheet.write(row, col, celda)
                    col += 1
                row += 1
        elif self.__tipo == "cocinado":
            row = 0
            for dato in datos:
                worksheet.write(row, 0, dato)
                row += 1

    def cerrar_libro(self):
        self.__workbook.close()
