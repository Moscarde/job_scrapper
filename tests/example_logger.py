import os
import sys

# Adiciona o diretório pai ao sys.path para importar métodos.setup_logger
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from methods.setup_logger import get_logger

# Instancia o logger para este script de exemplo
logger = get_logger("example")
# A partir daqui, usamos o logger para registrar mensagens em diferentes níveis de severidade.
# logger.debug() para mensagens de depuração detalhadas
# logger.info() para eventos normais,
# logger.warning() para situações inesperadas,
# logger.error() para erros capturados, e
# logger.critical() para erros graves que comprometem a execução

# --- DEBUG: informações detalhadas de execução interna ---
logger.debug("Iniciando scraper — modo debug ativo")

# --- INFO: eventos normais do fluxo da aplicação ---
logger.info("Conectando ao endpoint: https://workingnomads.com/jobs")
logger.info("3 vagas encontradas para a query 'python remote'")

# --- WARNING: algo inesperado, mas a execução continua ---
logger.warning("Endpoint 'remoteok' está inativo e será ignorado")

# --- ERROR: falha em uma operação, capturada com stack trace ---
try:
    data = {"jobs": None}
    total = len(data["jobs"])  # TypeError: 'NoneType' has no len()
except TypeError as e:
    logger.error("Falha ao processar resposta do endpoint: %s", e, exc_info=True)

# --- CRITICAL: erro grave que compromete a execução ---
logger.critical("Diretório 'lake/' não pôde ser criado — execução interrompida")
