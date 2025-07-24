# Ytdlp Advanced Downloader

Projeto Completo Para Download De Vídeos E Áudios De +1000 Sites Usando Ytdlp.

Funcionalidades:
1. Download De Vídeos/Áudios Em Múltiplos Formatos (mp4, mp3, mkv, webm, opus)

2. Seleção De Qualidade (480p, 720p, 1080p, best, worst)

3. Interface CLI Interativa E Modo Servidor Web

4. Download De Playlists Com Opções De Skip/Intervalo

5. Extração De Legendas E Thumbnails

6. Gerenciamento De Metadados Em JSON

7. Sistema De Filas Com Downloads Simultâneos

8. Suporte A Proxy/VPN

9. Atualização Automática

Instalação
1. Requisitos:
- Python 3.10+
- ffmpeg (Instalação Automática Via Ytdlp)

2. Configuração:
git clone https://github.com/phoenixsrd/yt-dlp-advanced.git
cd yt-dlp-advanced
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt

## Como Usar

Recursos Implementados:
1. Download De Vídeos/Áudios Em Múltiplos Sites

2. Suporte A Formatos: mp4, mp3, mkv, webm, opus

3. Seleção De Qualidade Personalizada

4. CLI Interativa Com Menu Passo A Passo

5. Download De Playlists Com Skip/Intervalo

6. Extração De Legendas E Thumbnails

7. Exibição De Metadados Durante O Download

8. Salvamento De Metadados Em JSON

9. Servidor Web Com Interface Amigável

10. Sistema De Filas Com Threading

11. Suporte A Proxy Configurável Via .env

12. Atualização Automática Do Ytdlp

13. Compatibilidade Multi-Plataforma

14. Logs Detalhados E Tratamento De Erros

Para Executar:
1. Modo CLI: `python main.py` (Seguir Prompts) Ou Com Argumentos

2. Modo Web: `python main.py` E Selecionar Opção 2, Depois Acessar A Url Fornecida

3. Opções Avançadas: 

4. Playlist Com Intervalo: python main.py --url "https://youtube.com/playlist?list=..." --playlist --interval 1:10

5. Áudio Em OPUS: python main.py --url "https://twitter.com/..." --type audio --format opus

6. Com Proxy: python main.py --url "https://tiktok.com/..." --proxy "http://user:pass@host:port"

7. Fila De Downloads: python main.py --url "https://exemplo.com/video1" "https://exemplo.com/video2" --queue
8. Atualizar O Ytdlp: python updateytdlp.py

O Projeto Está Totalmente Configurável Através Do Arquivo `.env` E Oferece Uma Experiência Completa Tanto Para Usuários Técnicos (CLI) Quanto Para Usuários Comuns (interface Web).
