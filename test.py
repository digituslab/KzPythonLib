from pdb import set_trace
from KzServer import KzListener
from KzServer import KzDefaultServer

# Unique listener class (subclass of KzListener)
class my_listener(KzListener):
    # This method will be called when listener requests
    # to get server instance.
    # User should return the appropriate server instance.
    def reqServer(self):
        return my_server()

# Unique server class (subclass of KzDefaultServer)
class my_server(KzDefaultServer):

    # This method will be called
    # when socket has received data from remote host.
    def receiveEvt(self,d):
        self.sendData(d + "\r\n")
        print(d)

    # This method will be called
    # when connection has established.
    # User can write their own code in this method.
    def Main(self):
        while True:
            pass

# execution of script starts from here
lsn = my_listener("localhost",5000)
lsn.runListener(10)

# This is a main loop.
# To prevent program termination, this infinite loop is necessary.
while True:
    pass
