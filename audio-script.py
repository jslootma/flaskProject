import requests  # pip install requests


# Code to classify the recorded WAV files
import os
from datetime import datetime
import csv
import librosa
import numpy as np
# import trained SVM model
from joblib import load

date_list = []
time_list = []

timestamp_csv_file = "timestamp.csv"
# Specify the directories
input_directory = "/home/beezyStudents/Documents/flaskProject/media/WAV/"
output_directory = "/home/beezyStudents/Documents/Timestamps_and_labels"  # Output directory won't be necessary, immediately write to database
hornet_list = []

model_path = "/home/beezyStudents/Documents/flaskProject/static/audio_models"


def process_wav_files(input_directory, output_directory):
    # Get a list of all files in the specified directory
    files = sorted(os.listdir(input_directory))
    
    # Filter out only the WAV files
    wav_files = [file for file in files if file.endswith(".wav")]

    # Iterate over each WAV file
    for wav_file in wav_files:
        # Process the WAV file
        output = process_single_wav(os.path.join(input_directory, wav_file))
        print(output)
        # If the output is equal to 'hornet', save timestamp and label in a new directory
        if output == 'Hornet':
            # split title into time and date to add in different columns  
            date_list = []
            time_list = []
            parts = wav_file.split("_")
            date_part = parts[0]
            date_part = date_part[4:]
            date_list.append(date_part)
        
            time_part = parts[1]
            time_part = time_part[:-4]
            time_list.append(time_part)
            # add to csv file
            write_to_csv(timestamp_csv_file, date_list, time_list)
            # Delete the WAV file after processing
            os.remove(os.path.join(input_directory, wav_file))
        else:
            os.remove(os.path.join(input_directory, wav_file))
    
            
def write_to_csv(csv_file, date_list, time_list):
    # data to CSV in append mode
    with open(csv_file, 'a', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
    # write in new row
        for date, time in zip(date_list, time_list):
            writer.writerow([date, time])


def process_single_wav(wav_filepath):
   
    # Load the trained SVM model
    svm_model = load(f'{model_path}/svm_model_label.joblib')
    
    # load in file
    print(wav_filepath)
    audio, sr = librosa.load(wav_filepath)
    
    # preprocess sound
    # Filter
    from scipy.signal import butter, filtfilt

    def butter_bandpass(data, lowcut, highcut, fs, order=5):
        """
        Design a bandpass filter.

        Args:
        - lowcut (float) : the low cutoff frequency of the filter.
        - highcut (float): the high cutoff frequency of the filter.
        - fs     (float) : the sampling rate.
        - order    (int) : order of the filter, by default defined to 5.
        """
        
        # calculate the Nyquist frequency
        nyq = 0.5 * fs
        
        # design filter
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band', analog=False)
        
        # returns the filter coefficients: numerator and denominator
        y = filtfilt(b, a, data)
        return y

    # Define the bandpass frequencies
    lowcut = 100  # Lower cutoff frequency
    highcut = 1000  # Higher cutoff frequency

    # Apply bandpass filter to the audio
    yf = butter_bandpass(audio, lowcut, highcut, sr, order=5)

    mfccs_features = librosa.feature.mfcc(y=yf, sr=sr, n_mfcc=20)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    mfccs_scaled_features = mfccs_scaled_features.reshape(-1, 20)
    
    audio_features = mfccs_scaled_features
    
    # run classifier
    # Predict class label for the audio sample
    predicted_label = svm_model.predict(audio_features)
    
    print(predicted_label)
    
    return predicted_label

    
def save_timestamp_and_label(wav_filename, file):
    # Create the output directory if it doesn't exist
    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Create a new file with the timestamp and label
    label = 'hornet'
    new_filename = f"{timestamp}_{label}.txt"
    with open(os.path.join(output_directory, new_filename), 'w') as file:
        file.write(f"Timestamp: {timestamp}\nLabel: {label}")

# def send_push_notification():
    # Initialize Pushbullet with your API key
    # pb = Pushbullet(pushbullet_api_key)
    # Send a push notification with the timestamp and label
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # title = "Hornet Detected!"
    # body = f"Hornet detected at {timestamp}"
    # pb.push_note(title, body)


# Call the function to process WAV files in the input directory
process_wav_files(input_directory, output_directory)

# detected_class = input("Enter the detected class: ")  # Replace this code with the script that defines the detected class [the api accepts Bee, Hornet, Other]
# url = f"http://127.0.0.1:5000/audio-detected/{detected_class}"  # URL to add detected class to the database, notice that 127.0.0.1 is the localhost IP address
# response = requests.post(url)  # POST request to add detected class to the database
# print(response.status_code) # 201 if successful added, 400 if invalid class
# print(response.json()) # {"message": "Detected class registered"} if successful added, {"message": "Invalid class detected"} if invalid class
