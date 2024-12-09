from robot import *

class Manager:
    def __init__(self):
        self.active_connections = {"mitsubishi":None, "kawasaki":None}

    def add_robot(self, name: str):
        self.active_connections[name] = Robot(target=name)

    def transmit(self, name: str, p1,p2):
        try:
            self.active_connections[name].send_data(p1,p2)
        except:
            print("No connection to robot")
    def receive(self, name: str):
        try:
            self.active_connections[name].receive_status()
        except:
            print("No connection to robot")

