# medaudit
A tool for auditing medical devices and healthcare infrastructure. 

The tool is written to audit networks, protocols and infrastructure that runs in hospitals. At the time of writing this, the tools supports HL7 protocol. 
The tool will support FHIR auditing in the near future. 

Here are the features of the tool:
* HL7 message sender 
* HL7 Scanner
* DOS Testing
* Traffic Analysis 
* Fuzzer (in progress)
* API support for sending HL7 Message 

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

