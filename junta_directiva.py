import requests
from bs4 import BeautifulSoup

URL = "https://www.ine.gob.gt/ine/institucion/organizacion/#1506616987343-077bfc72-f3b6"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
print(soup)