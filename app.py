import os.path
import datetime as dt

from flask import Flask, request, jsonify, render_template, flash  # pip install Flask
from flask_sqlalchemy import SQLAlchemy # pip install Flask-SQLAlchemy

app = Flask(__name__)
app.secret_key = "beezyStudents-secretKey101!"

# Define the database connection
db_name = "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"  # This will create a sqlite database.db file in the same directory as the app.py file
db = SQLAlchemy()


# Define the database models
class AudioDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # datetime = db.Column(db.String(100), nullable=False)
    # The datetime columns should be a datetime object, not a string
    datetime = db.Column(db.DateTime(timezone=True), nullable=False, unique=True)
    class_detected = db.Column(db.String(50), nullable=False)

    def __init__(self, class_detected):
        self.datetime = dt.datetime.now()
        self.class_detected = class_detected

    def __repr__(self):
        return f"dict(datetime={self.datetime}, class_detected={self.class_detected})"


class ImageTaken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False, unique=True)
    filename = db.Column(db.String(150), nullable=False)

    def __init__(self, filename):
        self.datetime = dt.datetime.now()
        self.filename = filename


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/take-picture", methods=["POST"])
def take_picture():
    """
    The POST request will trigger the camera to take a picture.
    The POST request doesn't need to send any data.
    :return: the file name of the picture taken inside the designated image folder
    """
    # Insert code here to take a picture
    # Possible to call a python script that takes a picture, using the subprocess module (don't forget to import it)
    # Make sure to print the filename in the take_picture.py script
    #    filename = subprocess.check_output(["python3", "take_picture.py"])
    #    filename = filename.decode("utf-8")
    # Make sure the python script you want to use to take pictures on the Rpi is executable
    #    chmod +x take_picture.py
    # Make sure the picture is saved in the designated image folder
    # Remove this filename statement once the subprocess is working
    filename = "image.jpg"
    # Optionally add the foldername, filename, and timestamp to the database, so they can be listed later on

    # Return the filename in the POST method response
    return jsonify({"message": "Picture taken successfully", "filename": filename}), 201


@app.route("/images/", methods=["Get"])
@app.route("/images/<string:file>", methods=["GET"])
def pictures(file=None, file_list=[file for file in os.listdir("static/images/")]):
    return render_template("images.html", file=file, images=file_list), 200


# A webinterface to register detection and check the detections
@app.route("/audio-detected/", methods=["GET", "POST"])
def audio():
    if request.method == "POST":
        data = request.form
        if data["class_detected"] not in ["Bee", "Hornet", "Other"]:
            flash("Invalid class detected", category="error")
            http_response_code = 400
        else:
            audio_detection = AudioDetection(data["class_detected"])
            db.session.add(audio_detection)
            db.session.commit()
            flash("Detected class registered", category="success")
            http_response_code = 201
    else:
        http_response_code = 200
    return render_template("audio-detected.html", values=AudioDetection.query.all()), http_response_code


@app.route("/audio-detected/<string:class_detected>", methods=["GET", "POST"])
def audio_class(class_detected):
    if request.method == "GET":
        if class_detected not in ["Bee", "Hornet", "Other"]:
            return jsonify({"message": "Invalid class detected"}), 400
        else:
            audio_detections = AudioDetection.query.filter_by(class_detected=class_detected).all()
            dict_audio_detections = {detection.datetime.strftime("%Y-%m-%d %H:%M:%S"): detection.class_detected for detection in audio_detections}
            return jsonify(dict_audio_detections), 200
    elif request.method == "POST":
        if class_detected not in ["Bee", "Hornet", "Other"]:
            return jsonify({"message": "Invalid class detected"}), 400
        audio_detection = AudioDetection(class_detected)
        db.session.add(audio_detection)
        db.session.commit()
        return jsonify({"message": "Detected class registered"}), 201


if __name__ == '__main__':
    print("Starting the application")
    print("Creating the database")
    with app.app_context():
        db.create_all()
    print("Running the application")
    app.run(debug=True, host="0.0.0.0")
