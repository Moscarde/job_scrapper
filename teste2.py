import requests
from bs4 import BeautifulSoup

url = "https://engenha.com/vagas?q=data+analyst%7Csenior"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 1. Pegamos o container principal pelo ID
container = soup.find(id="vagas-container")

if container:
    # 2. Buscamos todos os FILHOS diretos (cada vaga individual)
    # Tente 'div' primeiro. Se não funcionar, inspecione se são 'article' ou 'li'
    vagas_listadas = container.find_all('div', recursive=False)
    
    # Caso o find_all('div') venha vazio, tente pegar todos os articles:
    if not vagas_listadas:
        vagas_listadas = container.find_all('article')

    print(f"Total de vagas encontradas no container: {len(vagas_listadas)}")

    for i, vaga in enumerate(vagas_listadas, 1):
        # Limpamos o texto e usamos um separador para não grudar tudo
        info = vaga.get_text(separator=' | ', strip=True)
        
        # Tentamos pegar o link da vaga
        link_tag = vaga.find('a', href=True)
        link = link_tag['href'] if link_tag else "Sem link"

        print(f"--- Vaga {i} ---")
        print(f"Dados: {info[:150]}...") # Mostra o começo dos dados
        print(f"Link: {link}\n")
else:
    print("Não encontrei o elemento com id='vagas-container'. Verifique se o ID está correto no HTML.")