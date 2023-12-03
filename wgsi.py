import logging

from flask import Flask, render_template, jsonify, request

# Disable flask log
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

HOST_URL = '127.0.0.1'
HOST_PORT = 80

# Flask Application
app = Flask(__name__)

# Initial text data rendered
text_data = {'artist': '', 'title': ''}
# Initial timestamp data rendered
timestamp_data = {'timestamp': '00:00 / 00:00'}


# Html
@app.route('/')
def index():
    background_video_src = 'https://drive.google.com/uc?export=download&id=1ZivLekeIa9q600O2r0fbHhJmp91TxmuS'
    return render_template('index.html', background_video=background_video_src)


# API
@app.route('/change_text', methods=['POST'])
def change_text():
    global text_data
    new_artist = request.json.get('artist')
    new_title = request.json.get('title')
    text_data['artist'] = new_artist
    text_data['title'] = new_title
    return jsonify({'message': 'Text changed successfully'})


@app.route('/get_text', methods=['GET'])
def get_text():
    return jsonify(text_data)


@app.route('/change_timestamp', methods=['POST'])
def change_timestamp():
    global timestamp_data
    new_timestamp = request.json.get('timestamp')
    timestamp_data['timestamp'] = new_timestamp
    return jsonify({'message': 'Timestamp changed successfully'})


@app.route('/get_timestamp', methods=['GET'])
def get_timestamp():
    return jsonify(timestamp_data)


if __name__ == '__main__':
    print('Page:', 'http://' + HOST_URL + ":" + str(HOST_PORT))
    app.run(use_reloader=False, host=HOST_URL, port=HOST_PORT)

