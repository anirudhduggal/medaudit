from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#hl7 helper scripts
from .hl7Scripts import hl7_messageSender, hl7_portScanner, hl7_exhaust, hl7_maliciousServer

from multiprocessing import Process

# Create your views here.
@api_view(['GET', 'POST'])
def api_hl7_sendMessage_view(request,format=None):
    if request.method == 'GET':
        return Response("API loaded")
    elif request.method == 'POST':
            try:
                data = json.loads(request.body)

                ipAddress = data["ipAddress"]
                port = data["port"]
                message = data["message"]
                timeout = data["timeout"]
                if timeout ==0 or not timeout:
                    timeout =2

                messageSendObject = hl7_messageSender.Hl7Message()
                reply = messageSendObject.send(ipAddress, port, message, timeout)

                return Response(reply)
            except Exception as e:
                return Response("Exception at view level, details " + str(e))

@api_view(['GET', 'POST'])
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

            portScanObject = hl7_portScanner.Scan()
            reply = portScanObject.start(ipAddress,port,message,timeout)
            return Response(reply)

        except Exception as e:
            return Response("Exception in view: " + str(e))

@api_view(['GET', 'POST'])
def api_hl7_dosTest_view(request,format=None):

    if request.method == 'GET':
        return Response("API loaded")

    elif request.method == 'POST':
        try:

            data = json.loads(request.body)
            ipAddress = data["ipAddress"]
            port = data["port"]
            start = data["start"]

            #create a thread for running a DOS attack
            threadObject = Process(target=hl7_exhaust.startDOS, args=(ipAddress, port, start))

            if start == 1:
                #open file to keep track of DOS attack
                dosTrackingFile = open('api/networkFiles/dosTrackingFile.txt','w+')
                dosTrackingFile.write("1")
                dosTrackingFile.close()
                threadObject.start()
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
def api_hl7_maliciousServer_view(request,format=None):

    if request.method == 'GET':
        return Response("API loaded")

    elif request.method == 'POST':
        try:

            data = json.loads(request.body)
            port = data["port"]
            message = data["message"]
            start = data["start"]

            #create a thread for running a DOS attack
            threadObject = Process(target=hl7_maliciousServer.startServer, args=(port, message, start))
            threadObject.start()
            return Response("Process started")

            # return Response("Post is working")
        except Exception as e:
            return Response("Exception here: " + str(e))
