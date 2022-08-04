# xlsx_chef.py
import xlsxwriter

class xlsxChef:
    def __init__(self, nombre='XLSXprueba') -> None:
        self.__workbook = xlsxwriter.Workbook(nombre + '.xlsx')

    def escribir_hoja(self, datos:list, encabezados=(), nombre_hoja="") -> None:
        worksheet = self.__workbook.add_worksheet(nombre_hoja)
        col = 0
        if len(encabezados) == 0:
            encabezados = range(len(datos[0]))
        for encabezado in encabezados:
            worksheet.write(0, col, encabezado)
            col += 1
        row = 1
        for fila in datos:
            col = 0
            for celda in fila:
                worksheet.write(row, col, celda)
                col += 1
            row += 1
    
    def cerrar_libro(self):
        self.__workbook.close()
