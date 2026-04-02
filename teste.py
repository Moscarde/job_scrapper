import requests

url = "https://www.workingnomads.com/jobsapi/_search"

# Geralmente APIs de busca precisam de um corpo (payload)
# Se você não enviar nada, ela pode retornar erro ou os resultados padrão
payload = {
    "query": {
        "match_all": {}
    },
    "size": 50  # Quantidade de vagas que você quer buscar
}

# É boa prática enviar um User-Agent para não ser bloqueado imediatamente
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

try:
    # Fazendo a requisição POST
    response = requests.post(url, json=payload, headers=headers)
    
    # Verifica se a requisição deu certo (status 200)
    response.raise_for_status()
    
    # Converte o resultado diretamente para um dicionário Python
    data = response.json()
    
    # Navegando nos dados (o padrão costuma ser hits -> hits)
    jobs = data.get('hits', {}).get('hits', [])
    
    n=1
    for job in jobs:
        source = job.get('_source', {})
        title = source.get('title')
        company = source.get('company_name')
        print(f"Vaga {n}: {title} | Empresa: {company}")
        n = n+1

except requests.exceptions.HTTPError as err:
    print(f"Erro na requisição: {err}")