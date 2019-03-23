import socket
import logging

consoleOuputFileName = "hl7/networkFiles/hl7_portScanner.log"
GlobalScanMessageList = ["msh", "MSH", "MSH|^~\&|ADT1|MCM|LABADT|MCM|198808181126|SECURITY|ADT^A01|MSG00001-|P|2.6"]

class Hl7Message:

    def send(self,host, port, message, timeout):
        # timeout for the reply, if the reply is not received in timeout parameter, close connection

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        global consoleOuputFileName
        logging.basicConfig(filename=consoleOuputFileName, level=logging.DEBUG, filemode='w')

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #timeout = int(timeout)
            conn.settimeout(int(timeout))
            conn.connect((host, int(port)))

            # start and end block - used to define start and End of message in MLLP
            start_block = b'\x0b'
            end_block = b'\x1c'
            carriage_return = b'\x0d'

            # create message here
            msg = start_block.decode() + message + end_block.decode() + carriage_return.decode()

            # send message
            logging.debug("Sending Message: " + str(msg.encode()))
            conn.send(msg.encode())

            # recieve ack / nack message (buffer size 4096)
            try:
                ack = conn.recv(4096)
                if ack:
                    writeAck = ack.decode()
                    logging.debug("Recieved a reply: "+writeAck)
                    return writeAck
                else:
                    logging.debug("Recieved no reply ")
            except socket.timeout as e:
                logging.debug("Exception: "+str(e))
                return e
            conn.close()
        # send an exception if connection fails
        except socket.error as e:
            logging.debug("Exception: " + str(e))
            return e

class Scan:

    global consoleOuputFileName
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=consoleOuputFileName, level=logging.DEBUG, filemode='w')
    logging.debug("Message recieved ")

    def start(self, host, port, message="", timeout=2):

        hl7messageSenderObject = Hl7Message()

        if message == "":
            message = GlobalScanMessageList

        if port == 0:
            print("working here")
            logging.debug("Starting Scan for IP address: " + host + " on all ports")
            for scanPort in range(1,65535):
                for currentMessage in message:
                    print(consoleOuputFileName)
                    ack = hl7messageSenderObject.send(host, port, currentMessage, timeout)
                    if ack:
                        logging.debug("Message recieved "+currentMessage)
                    else:
                        continue
        else:
            logging.debug("Starting Scan for IP address: " + host + " on Port: " + port)
            for currentMessage in message:
                #logging.debug("Sending message "+currentMessage)
                ack =  hl7messageSenderObject.send(host,port,currentMessage,timeout)
                if ack:
                    logging.debug("Found open port on "+str(port))
                    logging.debug("Message " + str(message))
                    break
                else:
                    print(ack)