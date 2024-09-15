import socket
import time
from decoder import save_stream_as_mp4
from symphonicAPI import transcribe

class TelloDroneAPI:
    def __init__(self):
        self.commands = {
            's': 'back 20',
            'w': 'forward 20',
            'a': 'left 20',
            'd': 'right 20',
            'e': 'cw 20',
            'q': 'ccw 20',
            'r': 'up 20',
            'f': 'down 20',
            'z': 'takeoff',
            'x': 'land',
            '1': 'streamon',
            '2': 'streamoff',
            # Add more key-command mappings as needed
        }
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

    def initialize_stream(self):
        self.send_command("takeoff")
        with open('output.bin', 'wb') as file:
            t_end = time.time() + 10
            while time.time() < t_end:
                try:
                    data, server = self.sock.recvfrom(1518)
                    print(data)
                    file.write(data)
                except Exception as e:
                    print ('Unexpected error occurred while saving video: %s\n' % e)
                    break
            binary_video_data = ''
            with open('output.bin', 'rb') as f:
                binary_video_data = f.read()
            save_stream_as_mp4(binary_video_data, 'output_video.mp4')
            print(transcribe('output_video.mp4'))
                
if __name__ == "__main__":
    my_drone = TelloDroneAPI()

    print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')
    print('end -- quit demo.\r\n')

    while True: 
        try:            
            msg = input("")
            if 'end' in msg:
                my_drone.send_command("land")
                print ('...')
                my_drone.connection.close()  
                break
            if 'auto' in msg:
                my_drone.send_command("takeoff")
                my_drone.send_command("streamon")
                my_drone.send_command("land")
                print ('...')
                my_drone.connection.close()  
                break
            else:
                if msg in my_drone.commands:
                    my_drone.send_command(my_drone.commands[msg])
        except KeyboardInterrupt:
            print ('\n . . .\n')
            my_drone.connection.close()  
            break