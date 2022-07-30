# xlsx_chef.py
import xlsxwriter

class CvsCocinado:
    def __init__(self, nombre='CVSprueba') -> None:
        self.__workbook = xlsxwriter.Workbook(nombre + '.xlsx')

    def escribir_hoja(self, datos:list, nombre_hoja:str) -> None:
        worksheet = self.__workbook.add_worksheet(nombre_hoja)
        row = 1
        col = 1
        worksheet.write
        for x, y in datos:
            worksheet.write(row, col,     x)
            worksheet.write(row, col + 1, y)
            row += 1
    
    def cerrar_libro(self):
        self.__workbook.close()

prueba = CvsCocinado()
prueba.escribir_hoja([('2000', 3), ('2001', 6), ('2002', 10)], '1_01')
prueba.cerrar_libro()