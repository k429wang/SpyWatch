import socket
import threading
import cv2
import time

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
                        print ('LOOP FAILED %s\n' % e)
                        break
                print("BROKE OUT OF LOOP")

if __name__ == "__main__":
    my_drone = TelloDroneAPI()

    print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

    print('SpyWatch: port ')

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
