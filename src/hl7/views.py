from django.shortcuts import render
from .hl7Scripts import hl7_portScanner, hl7_messageSender, hl7_networkAnalyzer, hl7_exhaust
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from multiprocessing import Process

# Create your views here.
@csrf_exempt
def scanHl7Ports_view(request):
    if request.method == 'POST':
        ipAddress = request.POST.get("ipAddress_txt")
        port = request.POST.get("port_txt")
        timeout = request.POST.get("timeout_txt")
        if timeout==0 or not timeout:
            timeout =2
        if not port:
            port =0
        print("Input Received:")
        print(str(ipAddress))
        print(str(port))
        print(str(timeout))

        consoleOuputFileName = "hl7/networkFiles/hl7_portScanner.log"
        obj = hl7_portScanner.Scan()
        obj.start(ipAddress,port,"",timeout)

        with open(consoleOuputFileName, 'r') as hl7PortScannerFile:
            data = hl7PortScannerFile.read()
        log_text = data
        return render(request, "scanHL7Ports.html", context={'text': log_text})
    else:
        return render(request, "scanHL7Ports.html", context={'text': 'Ready to test!'})

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
        obj.send(ipAddress,port,message,timeout)

        with open(consoleOuputFileName, 'r') as hl7MessageSenderFile:
            data = hl7MessageSenderFile.read()
        log_text = data
        return render(request, "sendMessage.html", context={'text': log_text})
    else:
        return render(request, "sendMessage.html", context={'text': 'Ready to test!'})

@csrf_exempt
def analyzeTraffic_view(request):
    if request.method == 'POST' and request.FILES['networkFile']:
        networkFile = request.FILES['networkFile']
        fs = FileSystemStorage()
        filename = fs.save(("hl7/networkFiles/"+networkFile.name), networkFile)
        uploaded_file_url = fs.url(filename)

        obj = hl7_networkAnalyzer.hl7Traffic()
        trafficDumpFile = obj.analyze(uploaded_file_url)
        finalUploadedFile = "networkFiles/"+trafficDumpFile

        return render(request, 'trafficAnalysis.html', {
            'uploaded_file_url': finalUploadedFile
        })
    return render(request, 'trafficAnalysis.html')

@csrf_exempt
def exhaustHl7Ports_view(request):
    if request.method == 'POST':
        ipAddress = request.POST.get("ipAddress_txt")
        port = request.POST.get("port_txt")
        start = request.POST.get("start_txt")

        print("Input Received:")
        print(str(ipAddress))
        print(str(port))
        print(str(start))

        threadObject = Process(target=hl7_exhaust.startDOS, args=(ipAddress, port, start))
        threadObject.start()

        with open('hl7/networkFiles/hl7_exhaust.log', 'r') as hl7exhaustFile:
            data = hl7exhaustFile.read()
        log_text = data
        return render(request, "exhaustHl7Ports.html", context={'text': log_text})
    else:
        return render(request, "exhaustHl7Ports.html", context={'text': 'Ready to test!'})

@csrf_exempt
def about_view(request):
    if request.method == 'GET':
        return render(request, "about.html")

@csrf_exempt
def fuzzer_view(request):
    if request.method == 'POST':
        ipAddress = request.POST.get("ipAddress_txt")
        port = request.POST.get("port_txt")

        message = request.POST.get("message_send_txt")
        consoleOuputFileName = "hl7_messageSender.log"
        print("Input Received:")
        print(str(ipAddress))
        print(str(port))
        print(str(message))

        obj = hl7_messageSender.Hl7Message()
        obj.send(ipAddress, port, message, consoleOuputFileName)

        with open('hl7_messageSender.log', 'r') as hl7MessageSenderFile:
            data = hl7MessageSenderFile.read()
        log_text = data
        return render(request, "fuzzer.html", context={'text': log_text})
    else:
        return render(request, "fuzzer.html", context={'text': 'Ready to test!'})

from django.shortcuts import redirect

def view_404(request):
    # make a redirect to homepage
    # you can use the name of url or just the plain link
    return redirect('/about') # or redirect('name-of-index-url')