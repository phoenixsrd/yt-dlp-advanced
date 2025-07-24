import argparse
from core.downloader import Downloader
from core.config import Config
from core.utils import logger, update_yt_dlp

def main():
    parser = argparse.ArgumentParser(description='CLI Avançada Para Ytdlp')
    parser.add_argument('url', nargs='*', help='URL(s) Do(s) Vídeo(s)')
    parser.add_argument('--type', choices=['video', 'audio', 'both'], default='video', help='Tipo De Download')
    parser.add_argument('--quality', default='best', help='Qualidade (480,720,1080,best,worst)')
    parser.add_argument('--format', default='mp4', choices=['mp4', 'mkv', 'webm', 'mp3', 'opus'], help='Formato De Saída')
    parser.add_argument('--output', default=Config.DOWNLOAD_DIR, help='Diretório De Saída')
    parser.add_argument('--playlist', action='store_true', help='Download De Playlist')
    parser.add_argument('--skip', type=int, help='Número De Itens Para Pular Na Playlist')
    parser.add_argument('--interval', type=str, help='Intervalo De Itens (Ex: 1:10)')
    parser.add_argument('--subtitles', action='store_true', help='Extrair Legendas')
    parser.add_argument('--thumbnail', action='store_true', help='Extrair Thumbnail')
    parser.add_argument('--metadata', action='store_true', help='Salvar Metadados')
    parser.add_argument('--proxy', help='Configurar Proxy')
    parser.add_argument('--update', action='store_true', help='Atualizar Ytdlp')
    parser.add_argument('--queue', action='store_true', help='Usar Sistema De Fila')

    args = parser.parse_args()

    if args.update:
        if update_yt_dlp():
            print("Ytdlp Atualizado Com Sucesso!")
        else:
            print("Erro Na Atualização. Verifique Os Logs.")

    if not args.url:
        print("\nModo Interativo:")
        args.url = [input("URL Do Vídeo/Playlist: ").strip()]
        if not args.url[0]:
            logger.error("URL É Obrigatória")
            return

        args.type = input("Tipo [video/audio/both]: ").strip() or 'video'
        args.quality = input("Qualidade [480/720/1080/best/worst]: ").strip() or 'best'
        args.format = input("Formato [mp4/mkv/webm/mp3/opus]: ").strip() or 'mp4'
        args.output = input(f"Diretório De Saída [{Config.DOWNLOAD_DIR}]: ").strip() or Config.DOWNLOAD_DIR
        args.playlist = input("É Uma Playlist? [s/N]: ").lower() == 's'
        
        if args.playlist:
            args.skip = input("Itens Para Pular (Enter Para Nenhum): ") or None
            if args.skip:
                args.skip = int(args.skip)
            else:
                args.interval = input("Intervalo (Ex: 1:10): ") or None
                if args.interval:
                    args.interval = tuple(map(int, args.interval.split(':')))
        
        args.subtitles = input("Extrair Legendas? [s/N]: ").lower() == 's'
        args.thumbnail = input("Extrair Thumbnail? [s/N]: ").lower() == 's'
        args.metadata = input("Salvar Metadados? [s/N]: ").lower() == 's'
        args.proxy = input("Proxy (Ex: http://user:pass@host:port): ").strip() or None
        args.queue = input("Usar sistema de fila? [s/N]: ").lower() == 's'

    playlist_opts = {}
    if args.playlist:
        if args.skip:
            playlist_opts['skip'] = args.skip
        elif args.interval:
            playlist_opts['interval'] = args.interval

    downloader = Downloader(
        url=args.url[0],
        download_type=args.type,
        quality=args.quality,
        format=args.format,
        output_dir=args.output,
        proxy=args.proxy,
        subtitles=args.subtitles,
        thumbnail=args.thumbnail,
        metadata=args.metadata,
        playlist_options=playlist_opts
    )

    if args.queue:
        downloader.start_queue(args.url)
    else:
        for url in args.url:
            downloader.url = url
            info = downloader.download_single()
            if info:
                print(f"\nDownload Completo: {info['title']}")
                print(f"Formato: {info['ext']}")
                print(f"Duração: {info['duration_string']}")
                print(f"Uploader: {info['uploader']}")
                print(f"Visualizações: {info['view_count']}")

if __name__ == '__main__':
    main()