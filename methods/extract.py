import requests
import json
from methods.setup_logger import get_logger

logger = get_logger("extract")

class Extract:
    def __init__(self, urls, date, utils, path="bronze"):
        self.urls = urls
        self.path = path
        self.timestamp = date.get("timestamp")
        self.utils = utils
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }

    def _handle_api(self, endpoint, save_path):
        """Caso WorkingNomads: Envia POST e salva o JSON bruto"""
        payload = {"query": {"match_all": {}}, "size": 50}
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            with open(save_path.replace(".html", ".json"), "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            logger.info("JSON salvo com sucesso em: %s", save_path)
        except Exception as e:
            logger.error("Erro na API %s: %s", endpoint, e, exc_info=True)

    def _handle_html(self, endpoint, save_path):
        """Caso Engenha: Envia GET e salva o HTML bruto"""
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(response.text)
            logger.info("HTML salvo com sucesso em: %s", save_path)
        except Exception as e:
            logger.error("Erro no HTML %s: %s", endpoint, e, exc_info=True)

    def extractData(self, query, site_name):
        """Direciona para o método correto baseado no site"""
        data = self.urls.get(site_name)
        if not data or data.get("active") != 1:
            return
        
        query_folder = query.replace(" ", "_")
        ext = "json" if "jobsapi" in data["url"] else "html"
        file_path = f"{self.path}/{site_name}/{query_folder}/{self.timestamp}.{ext}"

        if "jobsapi" in data["url"]:
            self._handle_api(data["url"], file_path)
        else:
            endpoint = f"{data['url']}{query.replace(' ', '+')}"
            self._handle_html(endpoint, file_path)