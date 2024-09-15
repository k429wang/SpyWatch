import socket
import time
from decoder import save_stream_as_mp4
from symphonicAPI import transcribe

class TelloDroneAPI:
    def __init__(self):
        # Initialize UDP connection to Tello drone
        host = ''
        port = 9000
        droneaddr = (host,port) 
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        locaddr = ('0.0.0.0', 11111)
        self.sock.bind(locaddr)
        
        self.connection = socket.socket(socket.AF_INET, # Internet
                                        socket.SOCK_DGRAM) # UDP                                
        
        # Initialize API connection to Tello Drone API
        self.TELLO_UDP_IP = '192.168.10.1'
        self.TELLO_UDP_PORT = 8889
        
        self.connection.bind(droneaddr)
        
        # Test connection (possible responses: ok, error)
        print("\nEstablishing connection...\n")

        msg = "command".encode(encoding="utf-8") 

        self.connection.sendto(msg, (self.TELLO_UDP_IP, self.TELLO_UDP_PORT))

    def send_command(self, message):
        self.connection.sendto(message.encode(encoding="utf-8"), (self.TELLO_UDP_IP, self.TELLO_UDP_PORT))

        if message == "streamon":
            self.initialize_stream()
        elif message == "transcribe":
            self.transcribe()

    def initialize_stream(self):
        print("Initializing stream...")
        with open('output.bin', 'wb') as file:
            t_end = time.time() + 5
            while time.time() < t_end:
                try:
                    data, server = self.sock.recvfrom(1518)
                    print(data)
                    file.write(data)
                except Exception as e:
                    print ('Unexpected error occurred while saving video: %s\n' % e)
                    break
            binary_video_data = ''
            print("Reading binary data...")
            with open('output.bin', 'rb') as f:
                binary_video_data = f.read()
            print("Converting to mp4...")
            save_stream_as_mp4(binary_video_data, 'output_video.mp4')
            print("Waiting for Symphonic API response...")
            print(transcribe('output_video.mp4'))
            
if __name__ == "__main__":
    my_drone = TelloDroneAPI()

    print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')
    print('end -- quit demo.\r\n')

    while True: 
        try:            
            msg = input("")
            if 'end' in msg:
                print ('...')
                my_drone.connection.close()  
                break
            else:
                my_drone.send_command(msg)
        except KeyboardInterrupt:
            print ('\n . . .\n')
            my_drone.connection.close()  
            break
