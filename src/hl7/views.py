from django.shortcuts import render
from django.http import HttpResponse
from .hl7Scripts import hl7_portScanner, hl7_messageSender, hl7_networkAnalyzer, hl7_exhaust, hl7_maliciousServer, hl7_fuzzer
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from multiprocessing import Process

from medaudit.settings import BASE_DIR

# Create your views here.
def about_view(request):
    return render(request, "about.html")

@csrf_exempt
def dosAttack_view(request):
    if request.method == 'POST':
        ipAddress = request.POST.get("ipAddress_txt")
        port = request.POST.get("port_txt")
        start = request.POST.get("start_txt")

        print("Input Received:")
        print(str(ipAddress))
        print(str(port))
        print(str(start))

        if int(start) == 1:
            threadObject = Process(target=hl7_exhaust.startDOS, args=(ipAddress, port, start))
            threadObject.start()
            return render(request, "hl7/dosAttack.html", context={'text': "DOS Started"})
        elif int(start) == 0:
            threadObject = Process(target=hl7_exhaust.startDOS, args=(ipAddress, port, start))
            threadObject.start()
            return render(request, "hl7/dosAttack.html", context={'text': "Stopping DOS"})
    else:
        return render(request, "hl7/dosAttack.html", context={'text': 'Ready to test!'})

def fuzzer_view(request):
    demo_text ="To be completed"
    return render(request, "hl7/fuzzer.html", context={'text': demo_text})

@csrf_exempt
def maliciousServer_view(request):
    if request.method == 'POST':
        port = request.POST.get("port_txt")
        message = request.POST.get("message_send_txt")
        start = request.POST.get("start_txt")

        maliciousServerTrackingFileLocation = BASE_DIR + "/hl7/networkFiles/maliciousServerTrackingFile.txt"

        print("port "+port+" message "+message+" start "+start)
        if int(start) ==1:
            threadObject = Process(target=hl7_maliciousServer.startServer, args=(port, message, start, maliciousServerTrackingFileLocation))
            threadObject.start()
            return render(request, "hl7/maliciousServer.html", context={'text': "Server started on port "+port+" and is replying "+message})
        elif int(start) ==0:
            threadObject = Process(target=hl7_maliciousServer.startServer, args=(port, message, start,maliciousServerTrackingFileLocation))
            threadObject.start()
            return render(request, "hl7/maliciousServer.html", context={'text': "Server Stopped"})

        return render(request, "hl7/maliciousServer.html", context={'text': 'Ready to test!'})
    else:
        return render(request, "hl7/maliciousServer.html", context={'text': 'Ready to test!'})



@csrf_exempt
def portScanner_view(request):
    if request.method == 'POST':
        ipAddress = request.POST.get("ipAddress_txt")
        port = request.POST.get("port_txt")
        timeout = request.POST.get("timeout_txt")
        if timeout == 0 or not timeout:
            timeout = 2
        if not port:
            port = 0
        print("Input Received:")
        print(str(ipAddress))
        print(str(port))
        print(str(timeout))

        consoleOuputFileName =BASE_DIR+"/hl7/networkFiles/hl7_portScanner.log"
        obj = hl7_portScanner.Scan()
        obj.start(ipAddress, port, "", timeout)

        with open(consoleOuputFileName, 'r') as hl7PortScannerFile:
            data = hl7PortScannerFile.read()
        log_text = data
        return render(request, "hl7/portScanner.html", context={'text': log_text})
    else:
        return render(request, "hl7/portScanner.html", context={'text': 'Ready to test!'})

@csrf_exempt
def sendMessage_view(request):
    if request.method == 'POST':
        ipAddress = request.POST.get("ipAddress_txt")
        port = request.POST.get("port_txt")
        timeout = request.POST.get("timeout_txt")
        message = request.POST.get("message_send_txt")
        consoleOuputFileName = "hl7/networkFiles/hl7_messageSender.log"
        if timeout == 0 or not timeout:
            timeout = 2
        print("Input Received:")
        print(str(ipAddress))
        print(str(port))
        print(str(timeout))
        print(str(message))

        obj = hl7_messageSender.Hl7Message()
        obj.send(ipAddress, port, message, timeout)

        with open(consoleOuputFileName, 'r') as hl7MessageSenderFile:
            data = hl7MessageSenderFile.read()
        log_text = data
        return render(request, "hl7/sendMessage.html", context={'text': log_text})
    else:
        return render(request, "hl7/sendMessage.html", context={'text': 'Ready to test!'})

def trafficAnalysis_view(request):
    if request.method == 'POST' and request.FILES['networkFile']:
        networkFile = request.FILES['networkFile']
        fs = FileSystemStorage()
        filename = fs.save((BASE_DIR+"/hl7/networkFiles/" + networkFile.name), networkFile)
        uploaded_file_url = fs.url(filename)

        obj = hl7_networkAnalyzer.hl7Traffic()
        trafficDumpFile = obj.analyze(uploaded_file_url)
        finalUploadedFile = trafficDumpFile

        return render(request, 'hl7/trafficAnalysis.html', {
            'uploaded_file_url': finalUploadedFile
        })
    return render(request, 'hl7/trafficAnalysis.html')




