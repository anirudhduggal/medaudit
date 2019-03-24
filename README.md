# Medaudit
A tool for auditing medical devices and healthcare infrastructure. I wrote this tool becuase I could not find any tool that would help me assist in medical device auditing / pentesting. 

I also added the support for web API so we can use the skill set of web application testing to test medical devices. 

The tool is written to audit networks, protocols and infrastructure that runs in hospitals. At the time of writing this, the tools supports HL7 protocol. 
The tool will support FHIR auditing in the near future. 

Here are the features of the tool:
* HL7 message sender 
* HL7 Scanner
* DOS Testing
* Traffic Analysis 
* API Support for using Proxies (Burp, ZAP) and REST client (e.g. Postman)
* Fuzzer (ready for integration, running final tests)

To understand Pen testing medical devices, these talks will help -
<a href="https://www.youtube.com/watch?v=MR7cH44fjrc"> Blackhat Talk</a>
<a href="https://www.youtube.com/watch?v=3S6RQo-OQ24"> HITB Talk</a>
<a href="https://www.youtube.com/watch?v=BftxP_odT54"> Nullcon Talk</a>

<img src="https://github.com/anirudhduggal/medaudit/blob/master/screenshots/TrafficAnalysis.PNG"></img>
<i>A Screenshot of network analysis, the tool extracts HL7 traffic from a network capture file and point the message flow</i>

**Installation**
The project runs on python 3 and uses Django, Bootstrap 2.

For using the tool, install python 3 first and then install pip. 

Download the project/ unzip it. 

cd src/
pip install –r requirements.txt
python manage.py runserver 8082

Open your browser and navigate to 

http://127.0.0.1:8082/about/

You should see the GUI now. 

<img src="https://github.com/anirudhduggal/medaudit/blob/master/screenshots/overview.PNG"></img>

