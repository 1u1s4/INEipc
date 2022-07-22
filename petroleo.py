import nasdaqdatalink
NASDAQ_DATA_LINK_API_KEY = "JKnsdDbemtzwvLU8UsL9"
data = nasdaqdatalink.get('ODA/POILWTI_USD')
fecha_reporte = "2022-07"
mes_formato = {
    1:"Ene",
    2:"Feb",
    3:"Mar",
    4:"Abr",
    5:"May",
    6:"Jun",
    7:"Jul",
    8:"Ago",
    9:"Sep",
    10:"Oct",
    11:"Nov",
    12:"Dic"
}

print(data.loc["2014-11-30"]["Value"])