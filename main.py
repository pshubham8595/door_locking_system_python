import os

from flask import Flask, jsonify, request, after_this_request
import threading
import time

from flask_cors import cross_origin, CORS

from arduino_config import openLock
from face_verification import is_image_valid
from firebase_config import checkOpenLockStatus
UPLOAD_FOLDER = 'testImage'


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def poll_function():
    print("Polling Started ...")
    lockStatus = checkOpenLockStatus("user12345")
    if lockStatus:
        openLock(5)
    print("Polling Done ...")


def run_periodically(interval, stop_event):
    while not stop_event.is_set():
        poll_function()
        stop_event.wait(interval)


@app.route('/')
def home():
    return "Flask server is running!"


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():
    print("Upload file called")
    if 'file' not in request.files:
        print("No file part")
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'})
    else:
        print(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        is_valid, matched_image = is_image_valid(file_path, "verified_users")
        print(is_valid, matched_image)
        response_json = {'isUserValid': is_valid, "matchedUser": matched_image}

        @after_this_request
        def startSprinkler(response):
            if is_valid:
                openLock(5)
            return response

        return jsonify(response_json), 200


if __name__ == '__main__':
    # Create a stop event
    stop_event = threading.Event()

    # Create and start a thread for polling
    polling_thread = threading.Thread(target=run_periodically, args=(10, stop_event))
    polling_thread.start()

    try:
        # Start the Flask server
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        pass
    finally:
        # Set the stop event and wait for the thread to finish
        stop_event.set()
        polling_thread.join()
        print("Polling thread stopped.")