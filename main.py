
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytubefix import YouTube
import os

app = Flask(__name__)
CORS(app) # Fixes the Connection Error

# This tells us if the server is working
@app.route('/')
def home():
    return "API is Running Successfully!"

@app.route('/api/info', methods=['GET'])
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL"}), 400
    try:
        yt = YouTube(url)
        return jsonify({
            "status": "success",
            "title": yt.title,
            "thumbnail": yt.thumbnail_url
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download():
    url = request.args.get('url')
    fmt = request.args.get('format', 'mp4')
    try:
        yt = YouTube(url)
        stream = yt.streams.get_audio_only() if fmt == 'mp3' else yt.streams.get_highest_resolution()
        file_path = stream.download(output_path="/tmp")
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run()
