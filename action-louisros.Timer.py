#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import os

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)
              
def settimer_callback(hermes, intentMessage):
  
    v = int(intentMessage.slots.valeur.first().value) * 60   
    os.system("echo " + str(v) + " >/var/lib/snips/skills/timeForAlarm")  
    os.system("echo 25 >/sys/class/gpio/export")
    os.system("echo out >/sys/class/gpio/gpio25/direction")
    os.system("echo 1 >/sys/class/gpio/gpio25/value")
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, "c'est fait cher Maître")
    
def stoptimer_callback(hermes, intentMessage):  
    os.system("echo 25 >/sys/class/gpio/unexport")
    os.system("rm /var/lib/snips/skills/timeForAlarm")   
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, "c'est fait le rappel est supprimé")
    
    

if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h\
        .subscribe_intent("louisros:settimer",settimer_callback)\
        .subscribe_intent("louisros:stoptimer",stoptimer_callback).start()
       
