import socket

GlobalScanMessageList = ["msh", "MSH", "MSH|^~\&|ADT1|MCM|LABADT|MCM|198808181126|SECURITY|ADT^A01|MSG00001-|P|2.6"]

class Hl7Message:
    def send(self,host, port, message, timeout=2):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(int(timeout))
            conn.connect((host, int(port)))


            # start and end block - used to define start and End of message in MLLP
            start_block = b'\x0b'
            end_block = b'\x1c'
            carriage_return = b'\x0d'

            # create message here
            msg = start_block.decode() + message + end_block.decode() + carriage_return.decode()
            # send message
            conn.send(msg.encode())
            # recieve ack / nack message (buffer size 4096)
            ack = conn.recv(4096)

            if ack:
                writeAck = ack.decode()
                return writeAck
            else:
                print("not found")
                conn.close()
                return ""
        # send an exception if connection fails
        except socket.error as e:
            return "Exception: No Reply, Maybe the port is not replying or is not active"

class Scan:

    def start(self, host, port, message="", timeout=2):

        hl7messageSenderObject = Hl7Message()

        if message == "":
            message = GlobalScanMessageList

        if port == 0:
            for scanPort in range(1,65535):
                for currentMessage in message:
                    ack = hl7messageSenderObject.send(host, port, currentMessage, timeout)
                    if ack:
                        return "Message received "+currentMessage
                    else:
                        continue
        else:
            print("Starting Scan for IP address: " + host + " on Port: " + port)
            for currentMessage in message:
                print(currentMessage)
                ack = hl7messageSenderObject.send(host,port,currentMessage,timeout)
                if ack and ack !="":
                    return("Found open port on "+str(port)+" and using the message "+str(currentMessage))
                    break
                else:
                    print(ack)