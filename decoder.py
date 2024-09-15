import ffmpeg
import os

def save_stream_as_mp4(binary_data, output_file):
    # Save the binary data to a temporary file
    temp_video_file = 'temp_video_stream.bin'
    
    with open(temp_video_file, 'wb') as f:
        f.write(binary_data)

    try:
        # Use FFmpeg to convert the binary video file to MP4 format
        # Here, we're assuming the input binary data is in a standard video format (like H.264)
        ffmpeg.input(temp_video_file).output(output_file, vcodec='libx264').run()
    except ffmpeg.Error as e:
        print(f"Error occurred: {e.stderr.decode()}")
    finally:
        # Remove the temporary binary video file
        if os.path.exists(temp_video_file):
            os.remove(temp_video_file)

# Example usage:
# binary_data = ...  # Binary data from the video stream
# save_stream_as_mp4(binary_data, 'output_video.mp4')

binary_video_data = ''
with open('output.bin', 'rb') as f:
    binary_video_data = f.read()
save_stream_as_mp4(binary_video_data, 'output_video.mp4')
