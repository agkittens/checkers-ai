from robot import *

class Manager:
    def __init__(self):
        self.active_connections = {"mitsubishi":None, "kawasaki":None, "others":None}

    def add_robot(self, name: str):
        self.active_connections[name] = Robot()

    def transmit(self, name: str):
        self.active_connections[name].send_data()

    def receive(self, name: str):
        self.active_connections[name].receive_status()

