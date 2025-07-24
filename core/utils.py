import os
import logging
import platform
import subprocess
from datetime import datetime
from .config import Config

def setup_logger():
    Config.ensure_directories()
    log_file = os.path.join(Config.LOG_DIR, f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('yt-dlp-wrapper')

logger = setup_logger()

def is_termux():
    return 'termux' in platform.platform().lower()

def update_yt_dlp():
    try:
        subprocess.run(['pip', 'install', '--upgrade', 'yt-dlp'], check=True)
        logger.info("Ytdlp Atualizado Com Sucesso.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro Ao Atualizar Ytdlp: {e}")
        return False