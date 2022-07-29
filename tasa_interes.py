import requests
import xlrd
from datetime import datetime, timedelta
from datetimeLAAR import year_ago, month_after, date_mini, mes_by_ordinal
FECHA_REPORTE = datetime.today().strftime("%Y-%m")
FECHA_ANTERIOR = year_ago(FECHA_REPORTE)
# descarga de datos
DATA_URL = "https://banguat.gob.gt/sites/default/files/banguat/imm/imm04.xls"
with open('tasa_interes.xls', 'wb') as f:
    r = requests.get(DATA_URL, allow_redirects=True)
    f.write(r.content)
    f.close()
# 1996  - col 2
# enero - fil 5 
book = xlrd.open_workbook("tasa_interes.xls")
sh = book.sheet_by_index(0)

data = []
COL = int(FECHA_ANTERIOR.split("-")[0]) - 1994
for i in range(int(FECHA_ANTERIOR.split("-")[1]) + 4, 12 + 5):
    marca_temp = FECHA_ANTERIOR.split("-")[0] + "-" + mes_by_ordinal(str(i - 4).rjust(2, "0"))
    interes = sh.cell_value(rowx=i, colx=COL)
    if interes == "":
        interes = 0
    data.append((marca_temp, f"{100*interes:.2f}"))

COL = int(FECHA_REPORTE.split("-")[0]) - 1994
for i in range(5, int(FECHA_REPORTE.split("-")[1]) + 4 + 1):
    marca_temp = FECHA_REPORTE.split("-")[0] + "-" + mes_by_ordinal(str(i - 4).rjust(2, "0"))
    interes = sh.cell_value(rowx=i, colx=COL)
    if interes == "":
        interes = 0
    data.append((marca_temp, f"{100*interes:.2f}"))

for i in data:
    print(i)
