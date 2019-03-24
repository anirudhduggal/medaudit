from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .hl7Scripts import hl7_portScanner, hl7_messageSender, hl7_maliciousServer, hl7_exhaust

from multiprocessing import Process

# Create your views here.
def test():
    print("im here")

@api_view(['GET', 'POST'])
def test_view(request):
    try:
        return JsonResponse("API working",safe=False)
    except ValueError as e:
        return Response(e.args[0])

@api_view(['GET', 'POST'])
@csrf_exempt
def api_hl7_sendMessage_view(request,format=None):

    if request.method == 'GET':
        return Response("API loaded")

    elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                print(data["ipAddress"])
                print(data["port"])
                print(data["timeout"])
                print(data["message"])

                ipAddress = data["ipAddress"]
                port = data["port"]
                message = data["message"]
                timeout = data["timeout"]
                if timeout ==0 or not timeout:
                    timeout =2
                consoleOuputFileName = "hl7/networkFiles/hl7_messageSender.log"

                obj = hl7_messageSender.Hl7Message()
                obj.send(ipAddress, port, message, timeout)

                with open(consoleOuputFileName, 'r') as hl7MessageSenderFile:
                    data = hl7MessageSenderFile.read()
                log_text = data
                return Response(log_text)
                #return Response("Post is working")
            except Exception as e:
                return Response("Exception here: " + str(e))


@api_view(['GET', 'POST'])
@csrf_exempt
def api_hl7_hostScan_view(request,format=None):

    if request.method == 'GET':
        return Response("API loaded")

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data["ipAddress"])
            print(data["port"])
            print(data["timeout"])


            ipAddress = data["ipAddress"]
            port = data["port"]
            timeout = data["timeout"]
            message=data["message"]

            if timeout == 0 or not timeout:
                timeout = 2
            consoleOuputFileName = "hl7/networkFiles/hl7_portScanner.log"


            obj = hl7_portScanner.Scan()
            obj.start(ipAddress,port,message,timeout)

            with open(consoleOuputFileName, 'r') as hl7PortScannerFile:
                data = hl7PortScannerFile.read()
            log_text = data
            return Response(log_text)
            # return Response("Post is working")
        except Exception as e:
            return Response("Exception here: " + str(e))

@api_view(['GET', 'POST'])
@csrf_exempt
def api_hl7_dosTest_view(request,format=None):

    if request.method == 'GET':
        return Response("API loaded")

    elif request.method == 'POST':
        try:

            data = json.loads(request.body)
            print(data["ipAddress"])
            print(data["port"])
            print(data["start"])

            ipAddress = data["ipAddress"]
            port = data["port"]
            start = data["start"]

            #create a thread for running a DOS attack

            #obj = hl7_exhaust.exhaust()

            threadObject = Process(target=hl7_exhaust.startDOS, args=(ipAddress, port, start))

            if start ==1:
                #open file to keep track of DOS attack
                dosTrackingFile = open('api/networkFiles/dosTrackingFile.txt','w+')
                dosTrackingFile.write("1")
                dosTrackingFile.close()
                print("here1")
                threadObject.start()
                print("here2")
                return Response("Attack started")

            elif start==0:
                dosTrackingFile = open('api/networkFiles/dosTrackingFile.txt', 'w+')
                dosTrackingFile.write("0")
                dosTrackingFile.close()
                return Response("Attack Stopped")
            else:

                return Response("Invalid start code")
            # return Response("Post is working")
        except Exception as e:
            return Response("Exception here: " + str(e))

@api_view(['GET', 'POST'])
@csrf_exempt
def api_hl7_maliciousServer_view(request,format=None):

    if request.method == 'GET':
        return Response("API loaded")

    elif request.method == 'POST':
        try:

            data = json.loads(request.body)
            print("User Input ")
            print(data["port"])
            print(data["start"])
            print(data["message"])

            port = data["port"]
            message = data["message"]
            start = data["start"]

            #create a thread for running a DOS attack

            threadObject = Process(target=hl7_maliciousServer.startServer, args=(port, message, start))
            threadObject.start()
            print("Last view call")
            return Response("Attack started")

            # return Response("Post is working")
        except Exception as e:
            return Response("Exception here: " + str(e))
