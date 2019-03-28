import socket
import logging
import string,random

consoleOuputFileName = "../networkFiles/hl7_fuzzer.log"

def send(host, port, message, timeout):
    # timeout for the reply, if the reply is not received in timeout parameter, close connection

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    global consoleOuputFileName
    logging.basicConfig(filename=consoleOuputFileName, level=logging.DEBUG, filemode='w')

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # timeout = int(timeout)
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
                logging.debug("Recieved a reply: " + writeAck)
                return writeAck
            else:
                logging.debug("Recieved no reply ")
        except socket.timeout as e:
            logging.debug("Exception: " + str(e))
            return e
        conn.close()
    # send an exception if connection fails
    except socket.error as e:
        logging.debug("Exception: " + str(e))
        return e

def start_fuzzing(message, ip_address, port, mode):
    print("Fuzzing started")
    for i in range(0, 1024):
        new_message = new_locate_replace(message, mode, i)
        try:
            response = send(ip_address, port, new_message, 5)
            print("Response received for request " + str(i) + " \n" + response)
        except Exception as e:
            print("Possible crash at message: ", new_message , "\n Error: " + str(e) )
    print("Fuzzing complete")



def new_locate_replace(message,mode, count):
    final_str = ""
    str = message.split("|")
    for i in range(len(str)):
        if "<%FUZZ%>" in str[i]:
            if(mode == 1):
                replace = "A" * count
            if(mode == 2):
                replace = random.choice(string.ascii_letters) * count
            if(mode == 3):
                pattern = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                pattern_special = "!@#$%^&*"
                first = random.choice(pattern) * count
                h = ""
                for j in range(0, count):
                    h = h + random.choice(pattern_special)
                # second = h*random.choice(range(0, 10))
                replace = first + h
            if (i == (len(str) - 1)):
                final_str += replace
            else:
                final_str += replace + "|"
        else:
            #print("value is :" + str[i])
            if (i == (len(str) - 1)):
                final_str += str[i]
            else:
                final_str += str[i] + "|"
    #print("First string" + message)
    #print("Final string is " + final_str)
    return final_str










