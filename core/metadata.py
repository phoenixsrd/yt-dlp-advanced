import json
import os
from .config import Config
from .utils import logger

def save_metadata(info, output_dir):
    try:
        filename = f"{info['id']}.json"
        metadata_path = os.path.join(output_dir, filename)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=4)
        logger.info(f"Metadados Salvos Em {metadata_path}")
        return True
    except Exception as e:
        logger.error(f"Erro Ao Salvar Metadados: {e}")
        return False