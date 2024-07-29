from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from pytubefix import YouTube
import json, os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

def get_video_data(link):
    """
    Gets all the needed data from a given valid youtube link if the video exists or it's public.
    """
    yt = YouTube(link)
    title = yt.title
    thumbnail = yt.thumbnail_url
    channel = yt.author
    channel_url = yt.channel_url
    views = yt.views
    length = yt.length

    return {'title': title, 'channel': channel, 'channel_url': channel_url, 'thumbnail': thumbnail, 'views': views, 'length': length}

def get_video_file(link):
    yt = YouTube(link)
    audioFile = yt.streams.first()
    outFile = audioFile.download(output_path='static/media')
    # Make the new audio file
    base, ext = os.path.splitext(outFile)
    newFile = base.strip() + '.mp4'
    os.rename(outFile, newFile)
    return newFile

def get_audio_file(link):
    yt = YouTube(link)
    audioFile = yt.streams.filter(only_audio=True).first()
    outFile = audioFile.download(output_path='static/media')
    # Make the new audio file
    base, ext = os.path.splitext(outFile)
    newFile = base.strip() + '.mp3'
    os.rename(outFile, newFile)
    return newFile

@app.route('/video', methods=['POST'])
def download_video():
    if request.method == 'POST':
        try:
            print(request)
            data = request.get_json()
            videoLink = data.get('link')

        except(KeyError, json.JSONDecodeError):
            return jsonify({'error': 'Invalid data sent'}), 400
        
        try:
            # Gets the video title if it has one.
            videoData = get_video_data(videoLink)
            videoFile = get_video_file(videoLink)

            # Send the result to JS so the user can see it.
            file_name = os.path.basename(videoFile)
            file_path = os.path.join("static/media/", file_name)

            response_data = {
                    'file_name': file_name,
                    'video_data': videoData
                }

            return jsonify(response_data), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Invalid request method'}), 500

@app.route('/audio', methods=['POST'])
def download_audio():
    if request.method == 'POST':
        try:
            print(request)
            data = request.get_json()
            videoLink = data.get('link')

        except(KeyError, json.JSONDecodeError):
            return jsonify({'error': 'Invalid data sent'}), 400
        
        try:
            # Gets the video title if it has one.
            videoData = get_video_data(videoLink)
            audioFile = get_audio_file(videoLink)

            # Send the result to JS so the user can see it.
            file_name = os.path.basename(audioFile)
            file_path = os.path.join("static/media/", file_name)

            response_data = {
                    'file_name': file_name,
                    'video_data': videoData
                }

            return jsonify(response_data), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Invalid request method'}), 500

@app.route('/download/<file_name>', methods=['GET'])
def download(file_name):
    file_path = os.path.join("static/media/", file_name)

    def generate():
        with open(file_path, 'rb') as file:
            yield from file
        os.remove(file_path)
        print(f"Deleted file: {file_path}")

    return Response(generate(), mimetype="audio/mp3", headers={
        "Content-Disposition": f"attachment; filename={file_name}"
    })

@app.errorhandler(404)
def missing_page(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)