import requests
from bs4 import BeautifulSoup
URL = "https://www.ine.gob.gt/ine/institucion/organizacion/"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')
recuadros = soup.find_all("div", attrs={"class":"vc_tta-panel-body"})

salida = {}
for i in range(2):
    apartados = [texto.text for texto in recuadros[i].find_all("h3", attrs={"class":"vc_custom_heading"})]
    sub_apartados = [texto.text.replace(u'\xa0', u' ').replace("\nT", "T") for texto in recuadros[i].find_all("p", attrs={"style":"text-align: center;"})]
    if i == 0:
        titular_suplente = sub_apartados.replace().split("\nTitular")
        salida["JUNTA DIRECTIVA"] = dict(zip(apartados, sub_apartados))
    else:
        sub_apartados_replace = [i.replace("Subgerencia Técnica\n", "").replace("Subgerencia Administrativa Financiera\n", "") for i in sub_apartados]
        salida["GERENCIA"] = dict(zip(("Gerente", "Subgerente Técnico", "Subgerente Administrativo Financiero"), sub_apartados_replace))
for i in salida["JUNTA DIRECTIVA"]:
    print(i)
    print(salida["JUNTA DIRECTIVA"][i])