import string,random
import hl7_messageSender as messageSender

def start_fuzzing(message, ip_address, port, mode):
    obj = messageSender.Hl7Message()
    print("Fuzzing started")
    for i in range(0, 2048):
        new_message = new_locate_replace(message, mode, i)
        try:
            response = obj.send(ip_address, port, new_message, 5, "log_file.txt")
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






