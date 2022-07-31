import requests
import xml.etree.ElementTree as ET
from funcionesjo import mes_by_ordinal, hoy, year_ago
import descriptor

FORMATO = "%d/%m/%Y"
FECHA_REPORTE = hoy(FORMATO)
FECHA_ANTERIOR = year_ago(fecha=FECHA_REPORTE, formato=FORMATO)
# SOAP request URL
URL = "http://www.banguat.gob.gt/variables/ws/TipoCambio.asmx"
PAYLOAD = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <TipoCambioRango xmlns="http://www.banguat.gob.gt/variables/ws/">
      <fechainit>{}</fechainit>
      <fechafin>{}</fechafin>
    </TipoCambioRango>
  </soap12:Body>
</soap12:Envelope>""".format(FECHA_ANTERIOR, FECHA_REPORTE)
# headers
HEADERS = {
    'Content-Type': 'text/xml; charset=utf-8'
}
# POST request
response = requests.request("POST", URL, headers=HEADERS, data=PAYLOAD)
# parsear XML
with open("cambio.xml", "w") as f:
    f.write(response.text)
    f.close()
tree = ET.parse("cambio.xml")
root = tree.getroot()
# analisis de los datos
fecha_i = FECHA_ANTERIOR
mes_actual = "-".join((fecha_i.split("/")[2], mes_by_ordinal(fecha_i.split("/")[1])))
datos_mes = []
data_mean = []
i = 0
for cambio in root[0][0][0][0]:
    i += 1
    fecha_i = cambio[1].text
    mes_actual_i = "-".join((fecha_i.split("/")[2], mes_by_ordinal(fecha_i.split("/")[1])))
    # la ultima comparacion es para calcular el promedio del ultimo mes
    if mes_actual_i != mes_actual or i == len(root[0][0][0][0]):
        data_mean.append((mes_actual, sum(datos_mes)/len(datos_mes)))
        datos_mes = []
        mes_actual = mes_actual_i
    try:
        precio = float(cambio[2].text)
        datos_mes.append(precio)
    except Exception as e:
        None
for i in data_mean:
    print(i)
print(descriptor.cambio_del_quetzal(data_mean))