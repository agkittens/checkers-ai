import socket

class Robot:

    def __init__(self, target="mitsubishi"):
        if target == "mitsubishi":
            self.ip = "192.168.0.210"
            self.port = 10002
        else:
            self.ip = "192.168.0.220"
            self.port = 49152
        self.target = target

        self.host = "192.168.0.200"
        self.connection = None
        self.is_connected = False
        self.is_available = True

        self.connect()

    # ipM: 192.168.0.210
    # ipK: 192.168.0.220

    def connect(self):
        try:
            # Create a TCP/IP socket
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the server
            self.connection.connect((self.ip, self.port))
            self.is_connected = True
            print("Connecting to robot at {}:{}".format(self.ip, self.port))

            if self.connection:
                print('conncted to ' + self.target)

        except ConnectionRefusedError:
            print("Connection to robot at {}:{} refused".format(self.ip, self.port))
            self.is_connected = False
        except Exception as e:
            print("Failed to connect to robot at {}:{} due to error: {}".format(self.ip, self.port, str(e)))
            self.is_connected = False


    def send_data(self,p1,p2):
        if self.target == "kawasaki":
            data= str(7-p1[0])+str(p1[1]) +str(7-p2[0])+str(p2[1])
        elif self.target == "mitsubishi":
            data= str(7-p1[0])+str(7-p1[1]) +str(7-p2[0])+str(7-p2[1])

        if self.is_connected and self.is_available:
            bytes = data.encode('ascii')
            try:
                self.connection.sendall(bytes)
                print("Data sent to robot: {}".format(data))

            except Exception as e:
                print("Failed to send data to robot due to error: {}".format(str(e)))
        else:
            print("Not connected to the robot. Please connect first.")


    def receive_status(self):
        if self.is_connected:
            try:
                data = self.connection.recv(2048).decode()
                if data:
                    print(data)
                    self.is_available = True
                else:
                    print("No data received from robot.")
                    self.is_available = False

            except Exception as e:
                print("Failed to receive data from robot due to error: {}".format(str(e)))
        else:
            print("Not connected to the robot. Please connect first.")


