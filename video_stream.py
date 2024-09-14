import socket

class TelloDroneAPI:
    def __init__(self):
        
        self.UDP_IP = '192.168.10.1'
        self.UDP_PORT = 8889 # Send command/receive response
        self.tello_address = (self.UDP_IP, self.UDP_PORT)

        print("UDP IP: %s" % self.UDP_IP)
        print("UDP PORT: %s" % self.UDP_PORT)

        self.connection = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_DGRAM # UDP
                                )
        
        # Test connection
        print("Establishing connection..")

        msg = "command"
        msg = msg.encode(encoding="utf-8") 

        self.connection.sendto(msg, (self.UDP_IP, self.UDP_PORT))

        self.connection.bind(self.tello_address)

        while True:
            data, addr = self.connection.recvfrom(1024)
            print("received message: %s" % data)
            if data == "ok":
                print("Connection successful!")
                break
            elif data == "error":
                print("Connection failed!")
            else:
                print("Unknown error: ")

    def send_command(self, message):
        # Sending
        print("message: %s" % message)

        self.connection.sendto(message, (self.UDP_IP, self.UDP_PORT))

    def receive_command(self):
        # Receiving
        self.connection.bind((self.UDP_IP, self.UDP_PORT))

        while True:
            data, addr = self.connection.recvfrom(1024)
            print("received message: %s" % data)

if __name__ == "__main__":
    my_drone = TelloDroneAPI()
    my_drone.send_command()