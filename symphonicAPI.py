import requests
import io

# Assuming video.mp4 exists

def transcribe(file_path):
 
    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run"

    print("Opening file...")

    with open(file_path, 'rb') as video_file:
        video = io.BytesIO(video_file.read())

    print("Sending request...")

    response = requests.post(url, files={'video': ('output_video.mp4', video, 'video/mp4')})

    print("Done")

    return(response.text)

if __name__ == "__main__":
    print(transcribe("./output_video.mp4"))
