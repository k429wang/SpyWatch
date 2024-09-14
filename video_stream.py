import socket
import threading
import cv2

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
                                socket.SOCK_DGRAM # UDP
                                )
        
        self.TELLO_UDP_IP = '192.168.10.1'
        self.TELLO_UDP_PORT = 8889
        

        self.connection.bind(droneaddr)

        # Setup async thread to receive responses from drone
        def recv():
            count = 0
            while True: 
                try:
                    data, server = self.connection.recvfrom(1518)
                    print(data.decode(encoding="utf-8"))
                except Exception:
                    print ('\nExit . . .\n')
                    break

        recvThread = threading.Thread(target=recv)
        recvThread.start()
        
        # Test connection (possible responses: ok, error)
        # TODO: do i have to send this command before EVERY command, or just once at the beginning?
        print("Establishing connection..")

        msg = "command".encode(encoding="utf-8") 

        self.connection.sendto(msg, (self.TELLO_UDP_IP, self.TELLO_UDP_PORT))

    def send_command(self, message):
        # Sending
        print("command: %s" % message)

        self.connection.sendto(message.encode(encoding="utf-8"), (self.TELLO_UDP_IP, self.TELLO_UDP_PORT))
    
    def start_recording(self):
        self.connection.sendto("streamon".encode(encoding="utf-8"), (self.TELLO_UDP_IP, self.TELLO_UDP_PORT))
        

        while True: 
            try:
                data, server = self.sock.recvfrom(1518)
            except Exception:
                print ('\nExit . . .\n')
                break


    
    def switch_listening_port(self, port):
        self.TELLO_UDP_PORT = port

if __name__ == "__main__":
    my_drone = TelloDroneAPI()

    print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

    print('SpyWatch: port ')

    print ('end -- quit demo.\r\n')

    while True: 
        try:            
            msg = input("")
            if 'end' in msg:
                print ('...')
                my_drone.connection.close()  
                break
                
            if 'port' in msg:
                my_drone.switch_listening_port(msg)
            else:
                # Send data
                my_drone.send_command(msg)
                my_drone.start_recording()
        except KeyboardInterrupt:
            print ('\n . . .\n')
            my_drone.connection.close()  
            break
