
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
    "data engineer",
    "data analytics",
    "analytics engineer",
    "data architect",
    "big data engineer",
    "cloud data engineer",
    "database administrator",
    "engenheiro de dados",
    "business intelligence analyst",
    "analista de bi",
    "bi developer",
    "product data analyst",
    "marketing data analyst",
    "analista de dados",
    "reporting analyst",
    "data scientist",
    "cientista de dados",
    "machine learning engineer",
    "mlops engineer",
    "ai engineer",
    "data governance analyst",
    "data quality engineer"
}

#for query in queries:
#    extract.extractData(query=query)

transform = Transform()

directories = utils.listDir(f"{path}/{year}/{month}/{day}")

for directory in directories:
    files = utils.listDir(f"{path}/{year}/{month}/{day}/{directory}")
    for file_name in files:
        html_text = utils.loadFile(f"{path}/{year}/{month}/{day}/{directory}/{file_name}")
        soup = transform.soupHtml(html_text)
        #print(transform.getJobs(directory,soup))
        seletor = "html > body > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > main > section > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > a > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > h4"

        elemento = soup.select_one(seletor)
    if elemento:
        print(elemento.text)

