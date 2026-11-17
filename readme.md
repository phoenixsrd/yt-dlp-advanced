# ⬇️ yt-dlp Advanced

Camada prática sobre o `yt-dlp` para baixar vídeos e áudios de sites compatíveis. Oferece uma CLI com argumentos e modo interativo, uma interface web em Flask, seleção de qualidade, playlists, fila com downloads simultâneos, extração de legendas, thumbnails e metadados, além de proxy configurável.

> Baixe apenas conteúdo que você tem autorização para obter e respeite os termos de uso, direitos autorais e leis aplicáveis a cada serviço.

## Recursos

- Download de vídeo e áudio nos formatos `mp4`, `mkv`, `webm`, `mp3` e `opus`.
- Qualidade por altura máxima (`480`, `720`, `1080`), `best` ou `worst`.
- CLI com argumentos ou modo interativo, que pergunta cada opção.
- Interface web em Flask com formulário de download.
- Playlists com limite de itens ou intervalo.
- Legendas (todos os idiomas disponíveis), thumbnail e metadados salvos em JSON.
- Fila com downloads simultâneos (padrão: 3).
- Proxy por argumento ou variável de ambiente.
- Atualização do `yt-dlp` por comando ou script.
- Log de cada execução em arquivo.

## Estrutura

```text
main.py            Ponto de entrada: CLI se houver argumentos, senão menu
updateytdlp.py     Atualiza o yt-dlp via pip
cli/interface.py   Argumentos e modo interativo
core/config.py     Configurações lidas do .env
core/downloader.py Opções do yt-dlp, download único e fila
core/metadata.py   Gravação do JSON de metadados
core/utils.py      Logger e atualização do yt-dlp
web/server.py      Aplicação Flask
web/templates/     Página do formulário
.env               Valores padrão de configuração
requirements.txt   yt-dlp, Flask e python-dotenv
```

## Pré-requisitos

- Python 3.10 ou superior.
- `ffmpeg` no `PATH`, necessário para juntar vídeo e áudio e para extrair áudio em `mp3` ou `opus`.

## Instalação

```bash
git clone https://github.com/phoenixsrd/yt-dlp-advanced.git
cd yt-dlp-advanced
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows, ative o ambiente com `.venv\Scripts\activate`.

## Configuração

O `.env` já vem com os valores padrão. Todas as variáveis são opcionais.

| Variável | Padrão | Descrição |
|---|---|---|
| `DOWNLOAD_DIR` | `Download` | Pasta de destino dos arquivos |
| `LOG_DIR` | `logs` | Pasta dos logs (`download_AAAAMMDD_HHMMSS.log`) |
| `CONCURRENT_DOWNLOADS` | `3` | Downloads simultâneos no modo fila |
| `PROXY` | vazio | Proxy no formato `http://usuario:senha@host:porta` |
| `DEFAULT_FORMAT` | `mp4` | Lido pelo código, mas a CLI e o formulário web sempre enviam um formato, então hoje não tem efeito |
| `DEFAULT_QUALITY` | `best` | Lida em `core/config.py`, mas não é usada por nenhuma parte do programa |

O `.env` é versionado neste repositório. Se for usar proxy com usuário e senha, não coloque essas credenciais nele sem antes tirá-lo do controle de versão.

## Uso

### Menu

```bash
python main.py
```

Sem argumentos, o programa pergunta o modo: `1` para a CLI interativa ou `2` para o servidor web.

### CLI

As URLs são passadas diretamente, sem `--url`.

```bash
python main.py "https://exemplo.com/video"
python main.py "https://exemplo.com/video" --quality 720
python main.py "https://exemplo.com/video" --type audio --format mp3
python main.py "https://exemplo.com/video" --subtitles --thumbnail --metadata
python main.py "https://exemplo.com/video" --proxy "http://usuario:senha@host:porta"
python main.py "https://exemplo.com/video1" "https://exemplo.com/video2" --queue
python main.py --update
```

Sem nenhuma URL, a CLI entra no modo interativo e pergunta URL, tipo, qualidade, formato, pasta, playlist, legendas, thumbnail, metadados, proxy e fila. Isso vale também para `--update` sozinho: o `yt-dlp` é atualizado e, em seguida, o modo interativo começa.

| Argumento | Descrição |
|---|---|
| `url` | Uma ou mais URLs |
| `--type` | `video` (padrão), `audio` ou `both` |
| `--quality` | `480`, `720`, `1080`, `best` (padrão) ou `worst` |
| `--format` | `mp4` (padrão), `mkv`, `webm`, `mp3` ou `opus` |
| `--output` | Pasta de saída (padrão: `DOWNLOAD_DIR`) |
| `--playlist` | Trata a URL como playlist |
| `--skip N` | Em playlist, baixa os itens de 1 até N |
| `--interval` | Em playlist, intervalo de itens no formato `inicio:fim` |
| `--subtitles` | Baixa legendas |
| `--thumbnail` | Baixa a thumbnail |
| `--metadata` | Salva o JSON de metadados na pasta de saída, com o ID do vídeo como nome |
| `--proxy` | Proxy para a execução |
| `--update` | Atualiza o `yt-dlp` antes de baixar |
| `--queue` | Baixa as URLs em paralelo usando a fila |

### Interface web

Escolha `2` no menu. O servidor sobe em `0.0.0.0:5000`; acesse `http://localhost:5000`.

O formulário tem URL, tipo, qualidade, formato e as opções de legendas, thumbnail e metadados. O download roda em segundo plano e os arquivos ficam na pasta `DOWNLOAD_DIR`. A página só avisa que o download começou; não mostra progresso nem erros. Para usar proxy na interface web, defina `PROXY` no `.env`.

A interface não tem autenticação, e a rota `/downloads/<arquivo>` entrega qualquer arquivo da pasta `DOWNLOAD_DIR` a quem souber o nome. Se for acessá-la de outros aparelhos, use apenas em rede confiável.

### Atualizar o yt-dlp

```bash
python updateytdlp.py
```

## Comportamentos a conhecer

- `--type both` é aceito, mas hoje se comporta como `video`.
- Com `--type audio`, use `--format mp3` ou `opus`. Os formatos de vídeo (`mp4`, `mkv`, `webm`) não são codecs de áudio válidos para a extração.
- A qualidade não é validada: um valor que não seja número, `best` ou `worst` gera um formato inválido para o `yt-dlp`. Ela é ignorada em downloads de áudio.
- `--skip N` limita a playlist aos itens de 1 até N, e não pula os N primeiros.
- `--interval` funciona de forma confiável no modo interativo. Passado como argumento, o valor `inicio:fim` não é convertido em números e o download falha ao montar as opções.
- Na fila (`--queue`), as threads compartilham o mesmo objeto de download e o campo da URL atual. Com várias URLs ao mesmo tempo, alguma pode ser baixada mais de uma vez ou ficar de fora. Para conferir, veja os arquivos na pasta de saída.
- A interface web não oferece playlist, fila nem proxy no formulário.
- O suporte a sites, formatos e autenticação depende do `yt-dlp` instalado. Alguns sites podem exigir cookies ou configurações específicas, que não devem ser colocados no repositório.
