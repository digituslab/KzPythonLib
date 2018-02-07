# -*- coding:utf-8 -*-
#############################################################################
# Convenient TCP client class for robot operation
# Designed by Y.Watabe, Feb. 2, 2018
# Note!: This class can't handle the wide character.
#############################################################################
from pdb import set_trace   # for using the python embedded debugger.
from time import sleep
import socket
import threading
import re

# a Lock object for preventing to destroy the coherency of shared data.
m_client_lock = threading.Lock()

class KzClient:
    def __init__(self):         # constructor
        self.csock = None       # Socket for connection to server
        pass

    # Connect to server with following parameters.
    # adrs: IP address or URL string
    # port: Port number such as 5000
    # This method starts receiver loop thread automatically,
    # after establishing the connection with server.
    def connect(self,adrs,port):
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates socket object
        self.csock.connect((adrs, port))                                # Connects to server

        # Make thread for reading data from remote host
        rcvth = threading.Thread(target=self.rcvLoop, name="rcvth",args=())
        rcvth.daemon = True
        rcvth.start()

    def sendData(self,d):
        m_client_lock.acquire()
        b = d.encode('ascii')
        self.csock.send(b)
        m_client_lock.release()

    # This method will be called at the time of completion of receiving data from the server.
    # In most case, this method is overrided in subclass.
    def receiveEvt(self,d):
        print(d)

    # rcvLoop retrieves data stored in buffer from the server
    # and converts it to readable string then call the receiveEvt method.
    # <THREAD>
    def rcvLoop(self):
        ss = ""
        ky = ""
        while True:
            rcvmsg = self.csock.recv(1)
            ky = rcvmsg.decode('ascii')
            if(ky == "\r" or ky == "\n"):
                ss = re.sub(r"[\r\n]","*",ss)
                if ss != "":
                    self.receiveEvt(ss)
                ss = ""
            else:
                ss = ss + ky
