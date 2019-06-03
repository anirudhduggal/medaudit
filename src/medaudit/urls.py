"""medaudit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import api_hl7_sendMessage_view,api_hl7_hostScan_view, api_hl7_dosTest_view, api_hl7_maliciousServer_view
from hl7.views import sendMessage_view, portScanner_view,trafficAnalysis_view, dosAttack_view, about_view, fuzzer_view, maliciousServer_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about', about_view, name='About this tool'),

    path('hl7/sendMessage', sendMessage_view, name='Send HL7 Message'),
    path('hl7/scanHl7Ports', portScanner_view, name='Scan HL7'),
    path('hl7/analyzeTraffic', trafficAnalysis_view, name='Analyze Network Traffic'),
    path('hl7/exhaustHl7Ports', dosAttack_view, name='DOS Attack'),
    path('hl7/fuzzer', fuzzer_view, name='Fuzz HL7 Protocol'),
    path('hl7/maliciousServerTest', maliciousServer_view, name='Fuzz HL7 Protocol'),


    path('api/hl7/sendMessage', api_hl7_sendMessage_view, name='Send HL7 Message'),
    path('api/hl7/hostScan', api_hl7_hostScan_view, name='Scan a host'),
    path('api/hl7/dos', api_hl7_dosTest_view, name='Try a DOS test'),
    path('api/hl7/maliciousServerTest', api_hl7_maliciousServer_view, name='Start a malicious server'),
]
