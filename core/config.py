import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', 'Download')
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    PROXY = os.getenv('PROXY', None)
    CONCURRENT_DOWNLOADS = int(os.getenv('CONCURRENT_DOWNLOADS', 3))
    DEFAULT_FORMAT = os.getenv('DEFAULT_FORMAT', 'mp4')
    DEFAULT_QUALITY = os.getenv('DEFAULT_QUALITY', 'best')
    
    @classmethod
    def ensure_directories(cls):
        os.makedirs(cls.DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(cls.LOG_DIR, exist_ok=True)