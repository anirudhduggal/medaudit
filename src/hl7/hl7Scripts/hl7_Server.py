import socket

class server2x:

    def startServer(self,port,message):
        try:
            serverSocket = socket.socket()
            serverSocket.bind(('', port))

            serverSocket.listen(100)

            print("Server running on the port " + str(port))
            # start and end block - used to define start and End of message in MLLP
            start_block = b'\x0b'
            end_block = b'\x1c'
            carriage_return = b'\x0d'

            # create message here
            message = start_block.decode() + message + end_block.decode() + carriage_return.decode()

            while True:
                connection, address = serverSocket.accept()

                print("Got a connection from host at: ", str(address))
                print(message)
                connection.send(message.encode())
        except socket as e :
            print("Socket already occupied  "+e)

        except KeyboardInterrupt:
            connection.close()
