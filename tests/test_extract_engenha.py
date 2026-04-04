import os
import sys
from datetime import datetime

# SETUP DE CAMINHOS: Localiza a pasta /tests e a raiz do projeto
BASE_TEST_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(BASE_TEST_DIR)              
sys.path.insert(0, PROJECT_ROOT)

from methods.setup_logger import get_logger
from methods.extract import Extract
from methods.utils import Utils
from endpoints import sources

# Instância do Logger e Utils
logger = get_logger("test_engenha")
utils = Utils()

# Define o caminho do LAKE DE TESTE dentro da pasta tests
test_lake_root = os.path.join(BASE_TEST_DIR, "lake")
test_bronze = os.path.join(test_lake_root, "bronze")

def run_test():
    logger.info("🚀 Iniciando Teste de Extração: Engenha (HTML)")
    
    # 1. Parâmetros do teste
    query = "data engineer"
    site = "engenha"
    q_folder = query.replace(" ", "_")
    timestamp = f"test_{datetime.now().strftime('%H_%M')}"
    
    # --- AJUSTE: Garante a criação da árvore de pastas completa ---
    target_dir = os.path.join(test_bronze, site, q_folder)
    
    if not os.path.exists(target_dir):
        # Cria recursivamente: lake -> bronze -> engenha -> data_engineer
        os.makedirs(target_dir, exist_ok=True)
        logger.debug(f"Estrutura de pastas criada: {target_dir}")

    # 2. Configura o path relativo à raiz do projeto para o Extract
    # Isso resultará em 'tests/lake/bronze'
    relative_bronze_path = os.path.relpath(test_bronze, PROJECT_ROOT)

    extract = Extract(
        urls=sources,
        date={"timestamp": timestamp},
        utils=utils,
        path=relative_bronze_path
    )
    
    try:
        # 3. Executa a extração usando a lógica da classe oficial
        extract.extractData(query=query, site_name=site)
        
        # 4. VALIDAÇÃO: Verifica se o arquivo .html foi salvo
        expected_file = os.path.join(target_dir, f"{timestamp}.html")
        
        if os.path.exists(expected_file):
            size = os.path.getsize(expected_file)
            # Validamos se o HTML tem conteúdo (geralmente > 1000 bytes)
            if size > 500:
                logger.info("✅ SUCESSO: HTML de teste capturado: %s (%d bytes)", expected_file, size)
            else:
                logger.warning("⚠️ ALERTA: Arquivo criado, mas parece muito pequeno (%d bytes).", size)
        else:
            logger.error("❌ FALHA: O arquivo HTML esperado não foi encontrado em %s", expected_file)
            
    except Exception as e:
        logger.critical("💥 ERRO no teste do Engenha: %s", e, exc_info=True)

if __name__ == "__main__":
    run_test()