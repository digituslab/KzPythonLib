# -*- coding:utf-8 -*-
from KzClient import KzClient

class myClient(KzClient):
    def receiveEvt(self,d):
        rd = d.split(",")       # Convert string into array by comma.
        n = int(rd[-1])+1       # Retrieve last element in array and increment number.
        self.sendData("test," + str(n) + "\r\n")    # Send back data incremented to server.
        print(d)

cc = myClient()                 # Create instance of myClient class.
cc.connect("localhost",5000)    # Connet to localhost with port number 5000.
cc.sendData("test,1\r\n")       # Send data to server as initiation.

# This is a main loop.
# To prevent program termination, this infinite loop is necessary.
while True:
    pass
