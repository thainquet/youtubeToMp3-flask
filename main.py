from flask import Flask, request, jsonify, make_response
import youtube_dl

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [my_hook],
}

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World!'

# @app.route('/test')
# def test():
#     return 'Hello, World!'

@app.route('/get', methods=['GET'])
def get():
    url = request.args.get('url')
    filetype = request.args.get('type')
    print(url, filetype)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    resp = make_response(jsonify({"message": "ok"}), 200)
    return resp