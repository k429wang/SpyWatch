import socket
import threading
import cv2
import time
import base64
import keyboard

class TelloDroneAPI:
    def __init__(self):
        self.commands = {
            's': 'back 20',
            'w': 'forward 20',
            'a': 'left 20',
            'd': 'right 20',
            'e': 'cw 20',
            'q': 'ccw 20',
            'up': 'up 20',
            'down': 'down 20',
            't': 'takeoff',
            'l': 'land',
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
        
        self.TELLO_UDP_IP = '192.168.10.1'
        self.TELLO_UDP_PORT = 8889
        
        self.connection.bind(droneaddr)
        
        # Test connection (possible responses: ok, error)
        print("\nEstablishing connection...\n")

        msg = "command".encode(encoding="utf-8") 

        self.connection.sendto(msg, (self.TELLO_UDP_IP, self.TELLO_UDP_PORT))

    def send_command(self, message):
        # Sending
        self.connection.sendto(message.encode(encoding="utf-8"), (self.TELLO_UDP_IP, self.TELLO_UDP_PORT))

        if message == "streamon":
            with open('output.bin', 'wb') as file:
                t_end = time.time() + 1
                while time.time() < t_end:
                    try:
                        data, server = self.sock.recvfrom(1518)
                        print(data)
                        file.write(data)
                    except Exception as e:
                        print ('LOOP FAILED: %s\n' % e)
                        break
                print("BROKE OUT OF LOOP")
                
    def handle_key_press(self, key, command, delay=0.2):
        # Send command continuously while key is pressed
        while keyboard.is_pressed(key):
            self.send_command(command)
            time.sleep(delay)

if __name__ == "__main__":
    my_drone = TelloDroneAPI()

    print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

    print('SpyWatch: port ')

    print('end -- quit demo.\r\n')

    while True: 
        for key, command in my_drone.commands.items():
            if keyboard.is_pressed(key):
                # Start a new thread to handle continuous command sending
                threading.Thread(target=my_drone.handle_key_press, args=(key, command), daemon=True).start()

        # Exit the loop if 'm' is pressed
        if keyboard.is_pressed('m'):
            print("Exiting...")
            my_drone.send_command("land")
            break
