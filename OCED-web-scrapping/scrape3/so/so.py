import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página
url = "https://app.powerbi.com/view?r=eyJrIjoiNTUyNTk4YmUtN2U4Ny00N2MzLWFlM2UtYTY1ZGNhYTA5N2NmIiwidCI6IjFlZjViNjViLTkxYjktNGVjMS1iNmU0LTc3YTA1MzcxNTk1MyJ9"

# Realiza a requisição GET para obter o conteúdo da página
response = requests.get(url)
content = response.content

# Utiliza o BeautifulSoup para fazer o parsing do HTML
soup = BeautifulSoup(content, "html.parser")

# Encontra o elemento do código do iframe
iframe_element = soup.find("div", {"data-element-id": "elm_8HNLtJp5glVRnSc1LAaKwg"})

# Extrai o link do iframe
iframe_src = iframe_element.find("iframe")["src"]

# Realiza a requisição GET para obter o conteúdo do iframe
iframe_response = requests.get(iframe_src)
iframe_content = iframe_response.content

# Utiliza o pandas para ler os dados do iframe
df = pd.read_html(iframe_content)[0]

# Exibe o DataFrame
print(df)