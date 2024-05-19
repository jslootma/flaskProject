import os
import numpy as np
from gpiozero import MCP3008
import time
import wave
import signal
from datetime import datetime
import requests

# Specify the directory to save the recordings
WAV_dir = "/home/beezyStudents/Documents/flaskProject/media/WAV"

# Specify the channel on the ADC
mic = MCP3008(channel=0)
sample_rate = 48000  # 48 kHz
record_duration = 5  # 5-second recording duration

continue_recording = True


def end_recording(s, frame):  # Seems like signal and frame are unused, but function will receive 2 inputs
	global continue_recording
	print("Ctrl+C captured, ending recording.")
	continue_recording = False


signal.signal(signal.SIGINT, end_recording)


def get_init_recording_number():
	files = os.listdir(WAV_dir)
	files = [file for file in files if file.endswith('.wav')]
	return len(files) + 1


def record_and_save():
	recording_number = get_init_recording_number()
	while continue_recording:
		samples = []
		start_time = time.time()
		while time.time() < start_time + record_duration:
			samples.append(mic.value)
		print("Recording ended")
		actual_sample_rate = int(len(samples) / record_duration)
		print(f"Actual sample rate: {actual_sample_rate} samples per second")
		
		timestring = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		
		wav_filename = f"{recording_number:08}.{timestring}.wav"
		wav_filepath = os.path.join(WAV_dir, wav_filename)
		
		samples_arr = np.array(samples)
		num_frames = len(samples_arr)
		scaled_data = np.int16(samples_arr * 32767)
		with wave.open(wav_filepath, 'w') as wavfile:
			wavfile.setparams((1, 2, actual_sample_rate, num_frames, 'NONE', 'not compressed'))
			wavfile.writeframes(scaled_data.tobytes())
		print(f"WAV file #{recording_number} created")
		# Add to database
		requests.post("http://localhost:5000/audio-recorded/", json={"datetime": timestring, "filename": wav_filename})
		recording_number += 1


# Ensure the output directory exists
os.makedirs(WAV_dir, exist_ok=True)

# Main function to initiate recording
try:
	record_and_save()
except KeyboardInterrupt:
	pass  # Handle Ctrl+C KeyboardInterrupt
