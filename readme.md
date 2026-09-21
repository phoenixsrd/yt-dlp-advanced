# ⬇️ yt-dlp Advanced

O **yt-dlp Advanced Downloader** é uma ferramenta Python que oferece uma camada prática sobre o `yt-dlp` para baixar vídeos e áudios de muitos sites compatíveis. Ela combina uma CLI interativa, uma interface web Flask, seleção de qualidade, playlists, filas, metadados e configurações opcionais de proxy.

> Baixe apenas conteúdo que você tem autorização para obter e respeite os termos de uso, direitos autorais e leis aplicáveis a cada serviço.

## Recursos

- Download de vídeo e áudio em formatos como MP4, MP3, MKV, WebM e Opus.
- Seleção de qualidade (`480p`, `720p`, `1080p`, `best` e `worst`).
- CLI interativa para uso no terminal.
- Servidor web Flask para quem prefere uma interface no navegador.
- Playlists com opções de intervalo e skip.
- Extração de legendas, thumbnails e metadados em JSON.
- Filas e downloads simultâneos.
- Proxy configurável por argumento ou `.env`.
- Script separado para atualizar o `yt-dlp`.
- Logs e tratamento de erros para facilitar o acompanhamento.

## Como a aplicação inicia

`main.py` escolhe o modo de execução: quando recebe argumentos, encaminha o controle para `cli.interface`; sem argumentos, apresenta um menu para iniciar a CLI ou o servidor web. A lógica compartilhada fica separada em `core`, a interface web em `web` e os componentes da CLI em `cli`.

```text
main.py
├── cli/  → interface e argumentos do terminal
├── core/ → lógica de download, filas e configurações
└── web/  → servidor Flask e interface do navegador
```

## Pré-requisitos

- Python 3.10 ou superior.
- `ffmpeg` instalado e disponível no `PATH` para conversões e pós-processamento.
- Dependências do `requirements.txt`: `yt-dlp`, `Flask` e `python-dotenv`.

## Instalação

```bash
git clone https://github.com/phoenixsrd/yt-dlp-advanced.git
cd yt-dlp-advanced
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\\Scripts\\activate        # Windows
pip install -r requirements.txt
```

Se o projeto usar proxy ou outras opções externas, copie o `.env` de exemplo/configuração conforme a implementação atual e mantenha segredos fora do controle de versão.

## Executar

### Menu interativo

```bash
python main.py
```

Escolha `1` para a CLI ou `2` para o servidor web. O servidor é iniciado em `0.0.0.0:5000`; acesse `http://localhost:5000`.

### CLI com argumentos

```bash
python main.py --url "https://youtube.com/playlist?list=..." --playlist --interval 1:10
python main.py --url "https://exemplo.com/video" --type audio --format opus
python main.py --url "https://exemplo.com/video" --proxy "http://user:pass@host:port"
python main.py --url "https://exemplo.com/video1" "https://exemplo.com/video2" --queue
```

### Atualizar yt-dlp

```bash
python updateytdlp.py
```

## Observações

O suporte real a sites, formatos, autenticação e opções depende do `yt-dlp` instalado e do código em `core`. Alguns sites podem exigir cookies, autenticação ou configurações específicas. Nunca coloque cookies, tokens ou credenciais no repositório.
