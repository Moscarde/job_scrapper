import requests

class Extract:
    def __init__(self, urls, date, utils, path="lake"):
        self.urls = urls
        self.path = path
        self.year = date["year"]
        self.month = date["month"]
        self.day = date["day"]
        self.utils = utils
        # Adicionando headers para simular um navegador real
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def extractData(self, query="data engineer"):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        for site, data in self.urls.items():
            if data["active"] == 1:
                endpoint = data["url_q"] + query.replace(" ", "+")
                print(f"Extraindo de: {endpoint}")
                
                self.utils.createDir(f"{self.path}/{self.year}/{self.month}/{self.day}/{site}")

                # O SEGREDO ESTÁ AQUI: passar o headers
                html_response = requests.get(endpoint, headers=headers)
                
                if html_response.status_code == 200:
                    file_name_path = f"{self.path}/{self.year}/{self.month}/{self.day}/{site}/{query.replace(' ', '_')}.html"
                    with open(file_name_path, "w", encoding="utf-8") as f:
                        f.write(html_response.text)