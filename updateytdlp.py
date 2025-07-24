from core.utils import update_yt_dlp

if __name__ == '__main__':
    if update_yt_dlp():
        print("Ytdlp Atualizado Com Sucesso!")
    else:
        print("Falha Na Atualização. Verifique Os Logs.")