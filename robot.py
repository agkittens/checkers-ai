import socket

class Robot:

    def __init__(self):
        self.ip = ""
        self.port = 10001
        self.connection = None
        self.is_connected = False
        self.is_available = True

        # self.connect()

    # ipM: 192.168.0.210
    # ipK: 192.168.0.220

    def connect(self):
        print(self.ip)
        try:
            # Create a TCP/IP socket
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the server
            self.connection.connect((self.ip, self.port))
            self.is_connected = True
            print("Connected to robot at {}:{}".format(self.ip, self.port))

        except ConnectionRefusedError:
            print("Connection to robot at {}:{} refused".format(self.ip, self.port))
            self.is_connected = False
        except Exception as e:
            print("Failed to connect to robot at {}:{} due to error: {}".format(self.ip, self.port, str(e)))
            self.is_connected = False


    def send_data(self,p1,p2):
        data = p1
        if self.is_connected and self.is_available:
            try:
                self.connection.sendall(data.encode('ascii'))
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


if __name__ == "__main__":

    robot = Robot()
    robot.ip = '192.168.0.210'
    robot.port = 10001
    robot.connect()
    print(robot.is_connected, robot.is_available)

    while True:
            robot.send_data('test','aa')
            robot.receive_status()
