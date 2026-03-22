
from endpoints import urls
from datetime import datetime
from methods.utils import Utils

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


