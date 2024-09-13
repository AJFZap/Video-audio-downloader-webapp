from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from threading import Timer
from pytubefix import YouTube
import json, os, tempfile
import urllib.parse
# import logging

app = Flask(__name__, static_url_path='/static')

# logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

def get_video_data(yt):
    """
    Gets all the needed data from a given valid youtube link if the video exists or it's public.
    """
    title = yt.title
    thumbnail = yt.thumbnail_url
    channel = yt.author
    channel_url = yt.channel_url
    views = yt.views
    views = "{:,}".format(views) # Just to make the views more readable.
    length = yt.length

    return {'title': title, 'channel': channel, 'channel_url': channel_url, 'thumbnail': thumbnail, 'views': views, 'length': length}

def get_video_file(yt):
    """
    Download the video file from the given link.
    """
    audioFile = yt.streams.first()
    temp_dir = tempfile.gettempdir()
    outFile = audioFile.download(output_path=temp_dir)
    # logging.debug(f"Downloaded audio file to {outFile}")
    # Make the new audio file
    base, ext = os.path.splitext(outFile)
    newFile = base.strip() + '.mp4'
    os.rename(outFile, newFile)
    return newFile

def get_audio_file(yt):
    """
    Download the audio file from the given link.
    """
    audioFile = yt.streams.filter(only_audio=True).first()
    temp_dir = tempfile.gettempdir()
    outFile = audioFile.download(output_path=temp_dir)
    # logging.debug(f"Downloaded audio file to {outFile}")
    # Make the new audio file
    base, ext = os.path.splitext(outFile)
    newFile = base.strip() + '.mp3'
    os.rename(outFile, newFile)
    return newFile

@app.route('/video', methods=['POST'])
def download_video():
    """
    Gets the data and the video file and returns the name of the downloaded file and the data from the link.
    """
    if request.method == 'POST':
        with app.app_context():
            try:
                data = request.get_json()
                videoLink = data.get('link')
                yt = YouTube(videoLink)

            except(KeyError, json.JSONDecodeError):
                return jsonify({'error': 'Invalid data sent'}), 400
            
            try:
                # Gets the video title if it has one.
                videoData = get_video_data(yt)
                videoFile = get_video_file(yt)

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
    """
    Gets the data and the audio file and returns the name of the downloaded file and the data from the link.
    """
    if request.method == 'POST':
        with app.app_context():
            try:
                data = request.get_json()
                videoLink = data.get('link')
                yt = YouTube(videoLink)

            except(KeyError, json.JSONDecodeError):
                return jsonify({'error': 'Invalid data sent'}), 400
            
            try:
                # Gets the video title if it has one.
                videoData = get_video_data(yt)
                audioFile = get_audio_file(yt)

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

def encode_file_name(file_name):
    """
    We need to encode the file_name to be able to download it.
    To avoid errors we use URL encoding when is not posible to de the latin-1 encoding.
    """
    try:
        file_name.encode('latin-1')
    except UnicodeEncodeError:
        # If file_name cannot be encoded in latin-1, use URL encoding
        return urllib.parse.quote(file_name)
    return file_name

@app.route('/download/<file_name>', methods=['GET'])
def download(file_name):
    """
    Given the filename we download the file to the user PC and delete it from our media folder.
    """
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file_name)
    # logging.debug(f"Preparing to serve file from {file_path}")

    try:
        def generate():
            if not os.path.exists(file_path):
                with app.app_context():
                    return jsonify({'error': 'File not found'}), 404

            with open(file_path, 'rb') as file:
                yield from file
            
            # Schedule the file deletion after a short delay to ensure the response is sent
            Timer(10, lambda: os.remove(file_path)).start()
            # print(f"Deleted file: {file_path}")
        
        encoded_file_name = encode_file_name(file_name)
        content_disposition = f"attachment; filename={encoded_file_name}"

        return Response(generate(), mimetype="audio/mp3", headers={
            "Content-Disposition": content_disposition
        })
    except Exception as e:
        with app.app_context():
            return jsonify({'error': 'Failed to download file'}), 500

@app.errorhandler(404)
def missing_page(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=False)