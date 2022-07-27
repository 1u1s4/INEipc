import requests
import json
API_KEY = "515963d6-1153-e348-8394-a81acec0d6da"
#Llamado al API
url=f'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/00000/false/BISE/2.0/{API_KEY}?type=json'
response= requests.get(url)
if response.status_code==200:
    content= json.loads(response.content)
    print(content)