from flask import Flask, render_template, request, send_from_directory, after_this_request
import os
import threading
from core.downloader import Downloader
from core.config import Config
from core.utils import logger

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = Config.DOWNLOAD_DIR

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        download_type = request.form['type']
        quality = request.form['quality']
        file_format = request.form['format']
        
        downloader = Downloader(
            url=url,
            download_type=download_type,
            quality=quality,
            format=file_format,
            output_dir=app.config['DOWNLOAD_FOLDER'],
            subtitles='subtitles' in request.form,
            thumbnail='thumbnail' in request.form,
            metadata='metadata' in request.form
        )
        
        def download_task():
            with app.app_context():
                downloader.download_single()
        
        thread = threading.Thread(target=download_task)
        thread.start()
        
        return render_template('index.html', message="Download Iniciado! Verifique O Diretório De Downloads.")
    
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(
        app.config['DOWNLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)