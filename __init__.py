from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft import intent_handler
from adapt.intent import IntentBuilder
import json
import requests
import base64


 
class Createservice(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.s_messages = True
        self.d={}
        
    def initialize(self):
        def on_utterance(message):
            self.audio=message.data['signal']
            decode_string = base64.b64decode(self.audio.encode('utf-8'))
            
            send=base64.b64encode(decode_string).decode('ascii')
            self.d['audio']=json.dumps(send)
            self.d['tag'] = 'CreateService'

        self.add_event('recognizer_loop:utterance', on_utterance)
        
        
    @intent_handler('createservice.intent')   
    @adds_context('NameContext')
    def handle_createservice(self, message):

        self.name=""
        self.hosts=[]
        self.internet=False
        self.performance=[]
        response = requests.post('http://localhost:5550/sr/identification', json=self.d)
        res=response.json()
        id_=res['id']
        name_user=res['user_name']
        
        if(id_==1):
            self.speak('Sure '+name_user+'. What is the name of the service?​​',expect_response=True)
        elif(id_==0):
            self.speak(name_user+", you dont have permissions for that")
        else:
            self.speak("User not recognize")
        	

    
    @intent_handler(IntentBuilder('NameServiceIntent').require("Type").require('NameContext').build())
    @adds_context('HostsContext')
    def handle_name_service(self, message):
        utterance = message.data.get('Type')
        self.name=utterance
        self.log.info(utterance)
        self.speak('Sure. Please name the machines that will have access to the service​​​',expect_response=True)

    
    @intent_handler(IntentBuilder('HostsIntent').require('HostsContext').build())
    @adds_context('InternetAccessContext')
    def handle_hosts_service(self, message):
        utterance = message.data.get('utterance')
        res = [int(i) for i in utterance.split() if i.isdigit()]
        res=[str(x) for x in res]
        self.log.info(res)
        self.hosts=res
        self.speak('Regarding internet access, does the service need internet access?​​',expect_response=True)

        
    @intent_handler(IntentBuilder('YesInternetIntent').require("Yes").require('InternetAccessContext').build())
    @adds_context('PerformanceContext')
    @removes_context('InternetAccessContext')
    def handle_yes_internet_access(self, message):
        self.internet=True
        self.log.info(self.internet)
        self.speak('One last question, do you want to define the performance of the service?​​​',expect_response=True)

        
        
    @intent_handler(IntentBuilder('NoInternetIntent').require("No").require('InternetAccessContext').build())
    @adds_context('PerformanceContext')
    @removes_context('InternetAccessContext')
    def handle_no_internet_access(self, message):
        self.internet=False
        self.log.info(self.internet)
        self.speak('One last question, do you want to define the performance of the service?​​​',expect_response=True)

        
        
    @intent_handler(IntentBuilder('YesPerformanceIntent').require("Yes").require('PerformanceContext').build())
    @removes_context('NameContext')
    @removes_context('HostsContext')
    @removes_context('InternetAccessContext')
    def handle_yes_performance(self, message):
        utterance = message.data.get('utterance')
        res = [int(i) for i in utterance.split() if i.isdigit()]
        self.performance=res[0]
        self.log.info(res)
        self.speak('Thanks for the information, wait a bit while I implement the service​')
        json_={"IntentType": "CreateService","Intent_Target": "Service","Intent_State": "new intent","Conditions": [{"Policy": "CreateService","Constraints": [{ "Domains":[{"Name": self.name,"Bool": self.internet,"Acess": self.hosts,"Performance": self.performance}]}]}]}
        json_ = json.dumps(json_, indent = 4)  
        self.log.info(json_)   
        response = requests.post('http://localhost:5500/sr/intents', json=json_) 
        self.log.info(response.text)
        dictFromServer = response.json()


    
    @intent_handler(IntentBuilder('NoPerformanceIntent').require("No").require('PerformanceContext').build())
    @removes_context('NameContext')
    @removes_context('HostsContext')
    @removes_context('InternetAccessContext')
    def handle_no_performance(self, message):
        self.performance=0
        self.log.info(self.performance)
        self.speak('Thanks for the information, wait a bit while I implement the service​')
        json_={"IntentType": "CreateService","Intent_Target": "Service","Intent_State": "new intent","Conditions": [{"Policy": "CreateService","Constraints": [{ "Domains":[{"Name": self.name,"Bool": self.internet,"Acess": self.hosts,"Performance": self.performance}]}]}]}
        json_ = json.dumps(json_, indent = 4) 
        self.log.info(json_)
        response = requests.post('http://localhost:5500/sr/intents', json=json_)  
        self.log.info(response.text)
        dictFromServer = response.json()


        
    
    
def create_skill():
    return Createservice()

