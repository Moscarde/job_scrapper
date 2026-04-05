import json
import os
from endpoints import sources, queries
from datetime import datetime
from methods.utils import Utils
from methods.extract import Extract
from methods.transform import Transform
from methods.setup_logger import get_logger

# Instancia o logger do pipeline principal
logger = get_logger("app")

utils = Utils()
transform = Transform()

# --- Configurações de Caminho (Lake) ---
lake_root = "lake"
path_bronze = f"{lake_root}/bronze"
path_silver = f"{lake_root}/silver" 

today_str = datetime.now().strftime("%Y_%m_%d") 
timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M")

# 1. Garante que as pastas raiz existam
for folder in [lake_root, path_bronze, path_silver]:
    utils.createDir(folder)

# --- 2. LOOP DE PROCESSAMENTO ---
for site in sources.keys():
    if sources[site].get("active") == 1:
        for q in queries:
            q_folder = q.replace(" ", "_")
            
            bronze_dir = f"{path_bronze}/{site}/{q_folder}"
            silver_dir = f"{path_silver}/{site}/{q_folder}"
            
            utils.createDir(f"{path_bronze}/{site}")
            utils.createDir(bronze_dir)
            utils.createDir(f"{path_silver}/{site}")
            utils.createDir(silver_dir)

            # --- VERIFICAÇÃO DE EXISTÊNCIA ---
            existing_files = utils.listDir(silver_dir)
            already_done = any(f.startswith(today_str) for f in existing_files)

            if already_done:
                logger.info("[-] Check: Vagas para '%s' no site '%s' já processadas hoje. Pulando...", q, site)
                continue 

            # --- 3. EXTRAÇÃO ---
            logger.info("[+] Iniciando coleta: %s | %s", site, q)
            extract = Extract(
                urls=sources, 
                date={"timestamp": timestamp, "year": 2026, "month": 4, "day": 2}, 
                utils=utils, 
                path=path_bronze
            )
            
            extract.extractData(query=q, site_name=site)

            # --- 4. TRANSFORMAÇÃO IMEDIATA (SILVER) ---
            file_name = f"{timestamp}.html"
            if "jobsapi" in sources[site]["url"]:
                file_name = f"{timestamp}.json"

            try:
                raw_path = f"{bronze_dir}/{file_name}"
                raw_content = utils.loadFile(raw_path)
                
                vagas_processadas = transform.getJobs(site, raw_content)

                if vagas_processadas:
                    silver_path = f"{silver_dir}/{timestamp}.json"
                    with open(silver_path, "w", encoding="utf-8") as f:
                        json.dump(vagas_processadas, f, ensure_ascii=False, indent=4)
                    logger.info("    [OK] %d vagas salvas em Silver.", len(vagas_processadas))
            except Exception as e:
                logger.error("    [Erro] Falha ao processar %s/%s: %s", site, q, e, exc_info=True)

logger.info("--- Pipeline Finalizado ---")