import socket

def Server(port,message,maliciousServerTrackingFileLocation):
    while(True):
        maliciousServerTrackingFile = open(maliciousServerTrackingFileLocation, 'r')
        state = maliciousServerTrackingFile.read()
        maliciousServerTrackingFile.close()
        print("the state is "+str(state))

        try:
            if int(state) == 1:
                serverSocket = socket.socket()
                serverSocket.bind(('', int(port)))

                serverSocket.listen(100)

                print("Server running on the port " + str(port))
                # start and end block - used to define start and End of message in MLLP
                start_block = b'\x0b'
                end_block = b'\x1c'
                carriage_return = b'\x0d'

                # create message here
                message = start_block.decode() + message + end_block.decode() + carriage_return.decode()

                connection, address = serverSocket.accept()
                print("Got a connection from host at: ", str(address))
                print(message)
                connection.send(message.encode())
                connection.close()
            else:
                return

        except Exception as e :
            print("  "+str(e))

def startServer(port, message,start,maliciousServerTrackingFileLocation):
    print("in malicious server")
    print(str(port) + " " + str(message) + " ")
    if int(start) == 1:
        # open file to keep track of DOS attack
        maliciousServerTrackingFile = open(maliciousServerTrackingFileLocation, 'w+')
        maliciousServerTrackingFile.write("1")
        maliciousServerTrackingFile.close()
        print("server started")
        Server(port, message,maliciousServerTrackingFileLocation)

    elif int(start) == 0:
        maliciousServerTrackingFile = open(maliciousServerTrackingFileLocation, 'w+')
        maliciousServerTrackingFile.write("0")
        maliciousServerTrackingFile.close()
        print("server stopped")
        Server(port, message,maliciousServerTrackingFileLocation)

