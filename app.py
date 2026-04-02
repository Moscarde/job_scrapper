
from endpoints import urls
from datetime import datetime
from methods.utils import Utils
from methods.extract import Extract 
from methods.transform import Transform

#Configuração do Ambiente / Criação de Pastas
path = "lake"
year = datetime.now().year
month = datetime.now().month
day = datetime.now().day

utils = Utils()

utils.createDir(path)
utils.createDir(f"{path}/{year}")
utils.createDir(f"{path}/{year}/{month}")
utils.createDir(f"{path}/{year}/{month}/{day}")

extract = Extract(
    urls = urls,
    date = {
        "year": year,
        "month": month,
        "day": day
    },
    utils = utils,
    
)

queries = {
    # "data engineer",
    # "data analytics",
    "analytics engineer",
    # "data architect",
    # "big data engineer",
    # "cloud data engineer",
    # "database administrator",
    # "engenheiro de dados",
    # "business intelligence analyst",
    # "analista de bi",
    # "bi developer",
    # "product data analyst",
    # "marketing data analyst",
    # "analista de dados",
    # "reporting analyst",
    # "data scientist",
    # "cientista de dados",
    # "machine learning engineer",
    # "mlops engineer",
    # "ai engineer",
    # "data governance analyst",
    # "data quality engineer"
}

for query in queries:
    extract.extractData(query=query)

transform = Transform()
directories = utils.listDir(f"{path}/{year}/{month}/{day}")

for directory in directories: # directory aqui é o nome do site (ex: workingnomads)
    files = utils.listDir(f"{path}/{year}/{month}/{day}/{directory}")
    
    for file_name in files:
        print(f"\n--- Processando arquivo: {file_name} do site: {directory} ---")
        
        # Carrega o HTML salvo no Lake
        html_text = utils.loadFile(f"{path}/{year}/{month}/{day}/{directory}/{file_name}")
        
        # Transforma em Soup
        soup = transform.soupHtml(html_text)
        
        # Minera as vagas (Chama o handleWorkingNomads ou handleRemotar)
        vagas = transform.getJobs(directory, soup)
        
        # --- AQUI ENTRA O CÓDIGO QUE VOCÊ QUERIA COLOCAR ---
        if vagas:
            for v in vagas:
                print(f"Vaga encontrada: {v['title']} na empresa {v['company']}")
        else:
            print(f"Nenhuma vaga encontrada para {file_name}")