import os
from methods.setup_logger import get_logger

logger = get_logger("utils")

class Utils:
    def __init__(self):
        pass
    
    def createDir(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
            logger.debug("Diretório criado: %s", directory)
            
    def listDir(self, directory):
        try:
            return os.listdir(directory)
        except Exception as e:
            logger.error("Falha ao listar diretório %s: %s", directory, e, exc_info=True)
            return []
    
    def loadFile(self, file_name_path):
        try:
            with open(file_name_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error("Falha ao ler o arquivo %s: %s", file_name_path, e, exc_info=True)
            return ""