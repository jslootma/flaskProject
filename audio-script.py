import requests  # pip install requests

detected_class = input("Enter the detected class: ")  # Replace this code with the script that defines the detected class [the api accepts Bee, Hornet, Other]

url = f"http://127.0.0.1:5000/audio-detected/{detected_class}"  # URL to add detected class to the database, notice that 127.0.0.1 is the localhost IP address

response = requests.post(url)  # POST request to add detected class to the database

print(response.status_code) # 201 if successful added, 400 if invalid class
print(response.json()) # {"message": "Detected class registered"} if successful added, {"message": "Invalid class detected"} if invalid class