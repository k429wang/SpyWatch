import requests
import io

# Assuming video.mp4 exists

def transcribe(file_path):
 
    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run"

    print("Opening file...")

    with open(file_path, 'rb') as video_file:
        video = io.BytesIO(video_file.read())

    print("Sending request...")

    response = requests.post(url, files={'video': ('input.mp4', video, 'video/mp4')})

    print("Done")

    return(response.text)


print(transcribe("./watolink_short.mp4"))

# watolink is able to communicate with twitter through the twitter api and the tweepy python library. our program accesses twitter's api using the watolink's twitter api key.