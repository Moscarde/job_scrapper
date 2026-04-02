import json
import re
from bs4 import BeautifulSoup

class Transform:
    def __init__(self):
        pass
    
    def soupHtml(self, html_text):
        return BeautifulSoup(html_text, "html.parser") if html_text else None
    
    def getJobs(self, site_source, soup):
        if not soup:
            return []
        match site_source:
            case "workingnomads":
                return self.handleWorkingNomads(soup)
            case _:
                return []
            
    def handleWorkingNomads(self, soup):
        jobs_list = []
        
        # 1. Procuramos todos os blocos de script no HTML
        scripts = soup.find_all("script")
        
        for script in scripts:
            # 2. Procuramos o script que contém a definição da variável de jobs
            if script.string and 'jobs =' in script.string:
                # 3. Regex para capturar o conteúdo entre o '=' e o ';'
                # Isso isola o array JSON: [ { "id": 1, "title": "..." }, ... ]
                match = re.search(r'jobs\s*=\s*(\[.*\]);', script.string, re.DOTALL)
                
                if match:
                    try:
                        json_str = match.group(1)
                        data = json.loads(json_str)
                        
                        for item in data:
                            jobs_list.append({
                                "title": item.get("title", "N/A"),
                                "company": item.get("company_name", "N/A"),
                                "link": f"https://www.workingnomads.com/jobs/{item.get('id')}"
                            })
                        return jobs_list
                    except Exception as e:
                        print(f"Erro ao processar JSON: {e}")
        
        return []