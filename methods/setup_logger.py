import logging
import os
import sys
from datetime import datetime


def _get_project_root():
    """
    Retorna o caminho absoluto da raiz do projeto.

    Como esse arquivo fica em methods/, subimos dois níveis com dirname()
    para chegar na pasta raiz (onde ficam app.py, logs/, etc.).
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_log_dir():
    """
    Retorna o caminho da pasta logs/ e a cria caso não exista.

    O exist_ok=True evita erro se a pasta já tiver sido criada antes —
    útil quando o logger é instanciado várias vezes na mesma sessão.
    """
    log_dir = os.path.join(_get_project_root(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def _get_caller_slug():
    """
    Gera um identificador baseado no script que iniciou a execução.

    Usa sys.argv[0] para descobrir qual arquivo foi chamado no terminal
    (ex: app.py, tests/example_logger.py) e transforma o caminho relativo
    num slug sem extensão e com separadores substituídos por underscores.

    Exemplos:
        app.py                  -> "app"
        tests/example_logger.py -> "tests_example_logger"

    O bloco try/except cobre o caso de o script estar fora do projeto
    (ex: rodando num diretório completamente diferente), onde relpath()
    pode lançar ValueError no Windows.
    """
    entry_point = os.path.abspath(sys.argv[0])
    project_root = _get_project_root()
    try:
        rel_path = os.path.relpath(entry_point, project_root)
    except ValueError:
        rel_path = os.path.basename(entry_point)
    slug = os.path.splitext(rel_path)[0]
    slug = slug.replace(os.sep, "_").replace("/", "_")
    return slug


def get_logger(name: str) -> logging.Logger:
    """
    Cria e retorna um logger configurado para o nome informado.

    O logger escreve simultaneamente no terminal (StreamHandler) e num
    arquivo em logs/ (FileHandler). O nome do arquivo reflete o script
    de entrada e a data de hoje, ex: app_2026-04-02.log.

    A checagem de logger.handlers evita adicionar handlers duplicados
    se get_logger() for chamado mais de uma vez com o mesmo nome —
    o que seria um bug sutil causando linhas repetidas no log.

    Parâmetros:
        name (str): nome do logger, geralmente o módulo ou classe que
                    está usando. Ex: get_logger("extract"), get_logger("app").

    Retorno:
        logging.Logger: instância pronta para uso com os métodos
                        debug(), info(), warning(), error() e critical().
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    log_filename = f"{_get_caller_slug()}_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(_get_log_dir(), log_filename)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
