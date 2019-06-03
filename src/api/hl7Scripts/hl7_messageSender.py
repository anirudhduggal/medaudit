#hl72.x message sender class
import socket

class Hl7Message:
    def send(self,host, port, message, timeout):
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(int(timeout))
            conn.connect((host, int(port)))
            conn.setblocking(1)

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
                return "Received no reply"
            conn.close()
        # send an exception if connection fails
        except socket.error as e:
            return "Exception: No Reply, Maybe the port is not replying or is not active"