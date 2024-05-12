# README
This flask project provide a simple webapp and api to handle the api calls between the app and the audio and video python scripts.
## Requirements
Make sure to install the requirements from the requirements.txt file. If you encounter any errors, please install the requirements manually.
```bash
pip install -r requirements.txt
```
If you notice that certain requirements are not yet in the requirements.txt file, please contact the supervisors.

## Usage
To run the flask app, run the following command in the terminal (in the root folder of this project):
```bash
python app.py
```
The app will display the server ip:port in the terminal. You can access the webapp in the browser.<br>
Normally the localhost will certainly be included, the default port is 5000. <br>
[`Running on http://127.0.0.1:5000`](http://127.0.0.1:5000)

This will redirect you to the webapp's start page, showing `Hello World!`.

### Audio API
To use the audio api, you can use the following endpoints:
- `/audio-detected/<string:class_detected>` - POST request to upload a detected audio class *[Bee, Hornet, Other]*. The datetime will be added automatically.
- `/audio-detected/<string:class_detected>` - GET request to get all detected audio classes *[Bee, Hornet, Other]*.
  - This get method could be refined to handle query parameters, such as `?from=2021-01-01&to=2021-01-31` to get all detected audio classes between the given dates.

### Audio website
A simple webinterface is provided to manually upload detection and to view all detections in the database. The interface is available at
- `/audio-detected`

### Image API
To use the image api, you can use the following endpoints:
- `/take-picture` - POST request to take a picture and upload it to the server. The POST request returns a JSON object with the filename.
  - Here some work is still needed to make the image capturing work on the raspberry pi.
    - The python script that takes the picture should be called
    - The picture should be saved in the correct folder
    - The picturename should be stored in the database, a table ImageTaken that stores the datetime and filename is already created.

### Image website
A simple webinterface is provided to manually take a picture and to view all taken images in the database. The interface is available at
- `/images/` - website show the list of images available in the static/images folder.
  - If the images need to be stored elsewhere, the path should be changed in the `app.py` file.
- `/images/<string:file>` - website shows the image with the given filename. [If a picture is taken with the take-picture endpoint, the filename is returned in the JSON object and can be used to view the image.]
  - In the flutterflow app, this image URL can be used to load the image in the app.

## Database
The database is created using SQLalchemy and is a simple SQLite database. The database is stored in the `instance/database.db` file. The database contains two tables:
- `AudioDetected` - stores the datetime and detected audio class.
- `ImageTaken` - stores the datetime and filename of the taken image.

The database can be altered by changing the classes defined in the `app.py` file.

It is also possible to interact with the database using the `sqlite3` python package. However, the created api should provide all required functionality already.

## Flutterflow
In Flutterflow 2 API calls can be created:
- One to retrieve the audio detections
  - At this moment a GET call to `/audio-detected/Hornet` will return a JSON object with all datetimes of detected hornets. (This object can also be viewed from the browser)
    - Possibly This get method could be refined to handle query parameters, such as `?from=2021-01-01&to=2021-01-31` to get all detected audio classes between the given dates. However, this functionality is not yet implemented.
- One to take a picture
  - A POST call to `/take-picture` will take a picture and return a JSON object with the filename of the taken picture. This filename can be used to view the image in the browser or in the app.

