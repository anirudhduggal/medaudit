#hl72.x message sender class

import socket
import logging

consoleOuputFileName = "hl7/networkFiles/hl7_messageSender.log"

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