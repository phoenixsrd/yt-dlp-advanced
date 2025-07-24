import os
import yt_dlp
import threading
from queue import Queue
from .config import Config
from .utils import logger
from .metadata import save_metadata

class Downloader:
    def __init__(self, url, download_type='video', quality='best', format=None, output_dir=None, 
                 proxy=None, subtitles=False, thumbnail=False, metadata=False, playlist_options=None):
        self.url = url
        self.download_type = download_type
        self.quality = quality
        self.format = format or Config.DEFAULT_FORMAT
        self.output_dir = output_dir or Config.DOWNLOAD_DIR
        self.proxy = proxy or Config.PROXY
        self.subtitles = subtitles
        self.thumbnail = thumbnail
        self.metadata = metadata
        self.playlist_options = playlist_options or {}
        self.queue = Queue()
        self.threads = []
        self.setup_ydl_opts()

    def setup_ydl_opts(self):
        self.ydl_opts = {
            'proxy': self.proxy,
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'verbose': False,
            'ignoreerrors': True,
        }

        if self.download_type == 'audio':
            self.ydl_opts['format'] = 'bestaudio/best'
            self.ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.format,
            }]
        else:
            if self.quality == 'best':
                self.ydl_opts['format'] = 'bestvideo+bestaudio/best'
            elif self.quality == 'worst':
                self.ydl_opts['format'] = 'worstvideo+worstaudio/worst'
            else:
                self.ydl_opts['format'] = f'bestvideo[height<={self.quality}]+bestaudio/best'

            if self.format != 'mkv':
                self.ydl_opts['merge_output_format'] = self.format

        if self.playlist_options:
            if 'skip' in self.playlist_options:
                self.ydl_opts['playlist_items'] = f'1-{self.playlist_options["skip"]}'
            elif 'interval' in self.playlist_options:
                start, end = self.playlist_options['interval']
                self.ydl_opts['playlist_items'] = f'{start}:{end}'

        if self.subtitles:
            self.ydl_opts['writesubtitles'] = True
            self.ydl_opts['subtitleslangs'] = ['all']
        if self.thumbnail:
            self.ydl_opts['writethumbnail'] = True

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            logger.info(f"Progresso: {percent} | Velocidade: {speed} | ETA: {eta}")
        elif d['status'] == 'finished':
            logger.info("Download Concluído. Processando...")

    def download_single(self):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                if self.metadata and info:
                    save_metadata(info, self.output_dir)
                return info
        except Exception as e:
            logger.error(f"Erro No Download: {e}")
            return None

    def start_queue(self, urls):
        for url in urls:
            self.queue.put(url)
        
        for _ in range(Config.CONCURRENT_DOWNLOADS):
            t = threading.Thread(target=self._download_worker)
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        self.queue.join()

    def _download_worker(self):
        while True:
            url = self.queue.get()
            try:
                self.url = url
                self.download_single()
            finally:
                self.queue.task_done()