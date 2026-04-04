import json
import re
from bs4 import BeautifulSoup
from methods.setup_logger import get_logger

logger = get_logger("transform")

class Transform:
    def __init__(self):
        pass
    
    def soupHtml(self, html_text):
        return BeautifulSoup(html_text, "html.parser") if html_text else None
    
    def getJobs(self, site_source, raw_content):
        """
        Recebe o conteúdo bruto e direciona para o extrator específico.
        """
        if not raw_content or len(raw_content.strip()) == 0:
            return []

        match site_source:
            case "workingnomads":
                return self.handleWorkingNomads(raw_content)
            case "engenha":
                soup = self.soupHtml(raw_content)
                return self.handleEngenha(soup)
            case _:
                return []
            
    def handleWorkingNomads(self, json_data):
        """Trata o JSON bruto da API do WorkingNomads"""
        jobs_processed = []
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            items = data.get('hits', {}).get('hits', [])
            
            for item in items:
                source = item.get('_source', {})
                
                # Mapeamento padronizado para a Silver
                jobs_processed.append({
                    "hash_id": str(item.get("_id")), # Chave primária da API
                    "title": source.get("title", "N/A"),
                    "company": source.get("company", "N/A"),
                    "company_slug": source.get("company_slug", "N/A"),
                    "location": source.get("locations", ["Remote"])[0] if source.get("locations") else "Remote",
                    "url": source.get("apply_url") or f"https://www.workingnomads.com/jobs/{item.get('_id')}",
                    "salary_range": source.get("salary_range", "N/A"),
                    "experience_level": source.get("experience_level", "N/A"),
                    "site_source": "workingnomads"
                })
            
            logger.info("WorkingNomads: %d vagas processadas.", len(jobs_processed))
        except Exception as e:
            logger.error("Erro no Transform WorkingNomads: %s", e, exc_info=True)
        return jobs_processed

    def handleEngenha(self, soup):
        """Trata o HTML bruto do Engenha"""
        jobs_processed = []
        container = soup.find(id="vagas-container")
    
        if container:
            vagas_listadas = container.find_all(['div', 'article'], recursive=False)

            for vaga in vagas_listadas:
                link_tag = vaga.find('a', href=True)
                url = link_tag['href'] if link_tag else ""
            
                # Regex para extrair o ID (ex: ac-16115_4378857875)
                # Procuramos por algo que comece com 'ac-' e vá até a próxima barra '/'
                match = re.search(r'(ac-[\d_]+)', url)
                vaga_id = match.group(1) if match else "id_nao_encontrado"

                jobs_processed.append({
                    "hash_id": vaga_id, # <--- ESSA É SUA CHAVE DE OURO
                    "title": vaga.get_text(separator=' ', strip=True)[:100],
                    "url": url,
                    "site": "engenha"
                })
        return jobs_processed