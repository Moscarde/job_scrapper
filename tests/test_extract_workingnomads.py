import os
import sys
from datetime import datetime

# SETUP DE CAMINHOS
BASE_TEST_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(BASE_TEST_DIR)              
sys.path.insert(0, PROJECT_ROOT)

from methods.setup_logger import get_logger
from methods.extract import Extract
from methods.utils import Utils
from endpoints import sources

logger = get_logger("test_workingnomads")
utils = Utils()

# Define o caminho do LAKE DE TESTE
test_lake_root = os.path.join(BASE_TEST_DIR, "lake")
test_bronze = os.path.join(test_lake_root, "bronze")

def run_test():
    logger.info("🚀 Iniciando Teste de Extração: WorkingNomads (API)")
    
    # 1. Parâmetros do teste
    query = "analytics engineer"
    site = "workingnomads"
    q_folder = query.replace(" ", "_")
    timestamp = f"test_{datetime.now().strftime('%H_%M')}"
    
    # --- AJUSTE CRÍTICO: Criar a árvore de pastas completa para o teste ---
    # Isso evita o [Errno 2] pois garante que o diretório final exista
    target_dir = os.path.join(test_bronze, site, q_folder)
    
    if not os.path.exists(target_dir):
        # O os.makedirs com exist_ok=True cria todas as pastas intermediárias
        os.makedirs(target_dir, exist_ok=True)
        logger.debug(f"Pastas de teste criadas: {target_dir}")

    # 2. Configura o path relativo para o Extract
    relative_bronze_path = os.path.relpath(test_bronze, PROJECT_ROOT)

    extract = Extract(
        urls=sources,
        date={"timestamp": timestamp},
        utils=utils,
        path=relative_bronze_path
    )
    
    try:
        # 3. Executa a extração
        extract.extractData(query=query, site_name=site)
        
        # 4. Validação
        expected_file = os.path.join(target_dir, f"{timestamp}.json")
        
        if os.path.exists(expected_file):
            size = os.path.getsize(expected_file)
            logger.info("✅ SUCESSO: Arquivo de teste criado: %s (%d bytes)", expected_file, size)
        else:
            logger.error("❌ FALHA: Arquivo não encontrado em %s", expected_file)
            
    except Exception as e:
        logger.critical("💥 ERRO no teste: %s", e, exc_info=True)

if __name__ == "__main__":
    run_test()