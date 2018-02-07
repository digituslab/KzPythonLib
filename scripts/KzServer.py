# -*- coding:utf-8 -*-
#############################################################################
# Convenient TCP server class for robot operation
# Designed by Y.Watabe, Feb. 1, 2018
# Note!: This class can't handle the wide character.
#############################################################################
from pdb import set_trace   # for using the python embedded debugger.
from time import sleep
import socket
import threading
import re

# a Lock object for preventing to destroy the coherency of shared data.
m_lock = threading.Lock()

class KzListener:
    # Foundamental socket listener class.

    def __init__(self,adrs,prt):
        # Initialize class instance variables
        self.server_list = []   # container for prepared servers
        self.connected = 0      # number of connected clients
        self.host = adrs        # host IP address
        self.port = prt         # host port
        self.serversock = None  # socket object for server

        # Build up socket for server connection
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversock.bind((self.host,self.port))

    # startListen method waits connections from clients
    # and retrieves socket related to them.
    # <THREAD>
    def startListen(self,quemax):
        # Waits for connection from clients
        f = False
        cs = None   # socket for client
        self.serversock.listen(quemax)

        # an accept method blocks until socket has connected from client
        while True:
            csock, cadr = self.serversock.accept()
            print("IP=" + str(cadr) + "")
            cs = self.reqServer()
            if cs == None:
                print("Server instance is necessary to make connection.")
            else:
                self.server_list.append(cs)
                cs.linked = True     # Mark a linked flag to True
                cs.setSocket(csock)  # Set socket for communicating with client
                cs.runRcvLoop()
                # <todo> Call submain routine
                cs.subMainCaller()
                f = True

    # addServer method appends instance
    # which is holding the infomation of client socket into the container.
    def addServer(self,d):
        self.server_list.append(d)

    def reqServer(self):
        return None

    def runListener(self,quemax):
        th = threading.Thread(target=self.startListen,name="th",args=(quemax,))
        th.daemon = True    # kill the thread when the parent thread is terminated
        th.start()          # start the thread

        # main loop (to exit this loop, simply, press ctrl + C)
        # while True:
        #     sleep(0.1)
        #     None

class KzDefaultServer:
    # Initialization of this class.
    # At this initialization, set a link status to unlinked
    # and set null to the reference of a client socket.
    def __init__(self):
        self.linked = False # if this parameter is True, class has linked already to listner
        self.csock = None   # property for client socket
        None

    # Starts thread for reading data from the client connected to server.
    def runRcvLoop(self):
        self.linked = True  # set this object to "linked" state
        rth = threading.Thread(target=self.runThread,name="rth",args=()).start()

    def setSocket(self,d):
        self.csock = d

    # Thread for reading a data from remote client
    # This thread is started by runRcvLoop method.
    # <THREAD>
    def runThread(self):
        ss = ""     # receive buffer
        ky = ""     # var for 1 char
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

    # receiveEvt is invoked when a data from a client is settled.
    # In most case, this function should be inherited to custom class
    # to implement user's unique functionality.
    # <THREAD>
    def receiveEvt(self,d):
        pass

    def sendData(self,d):
        m_lock.acquire()
        b = d.encode('ascii')
        self.csock.send(b)
        m_lock.release()

    # subMainCaller calls Main method after conection with client is finished.
    # This method creates Main method as thread object.
    def subMainCaller(self):
        main_th = threading.Thread(target=self.Main,name="MainMain",args=())
        main_th.start()

    # Main method is equivalent to main function in C language.
    # Override this and Write connection specific code here.
    # <THREAD>
    def Main(self):
        pass
