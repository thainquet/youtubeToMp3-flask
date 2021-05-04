from flask import Flask, request, jsonify, make_response, send_from_directory, send_file
import youtube_dl
import os
import pathlib
import subprocess
import io
from multiprocessing import Process

basePath = pathlib.Path().absolute()


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/download', methods=['GET'])
def get():
    url = request.args.get('url')
    filename = ""
    resp = ""
    with youtube_dl.YoutubeDL({
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': "mp3",
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
    }) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    resp = make_response(
        jsonify({"message": "ok", "filename": filename.replace(".webm", ".mp3")}), 200)
    # if filetype == "mp4":
    #     subprocess.call(["youtube-dl","-f","18",url])
    return resp


@app.route('/check')
def check():
    filename = request.args.get('filename')
    file = os.path.join(os.getcwd(), os.listdir(os.getcwd())[0])
    fullPath = os.path.dirname(file) + '/' + filename
    # return send_from_directory(os.path.dirname(file), filename, as_attachment=True)
    return_data = io.BytesIO()
    with open(fullPath, 'rb') as f:
        return_data.write(f.read())
        return_data.seek(0)
        background_remove(fullPath)

    return send_file(return_data, mimetype='audio/mpeg',
                     attachment_filename=filename, as_attachment=True)


def background_remove(path):
    task = Process(target=rm(path))
    task.start()


def rm(path):
    os.remove(path)
