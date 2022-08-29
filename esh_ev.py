from turtle import color
from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

import os
import datetime
 
import math

import random
 
import base64

color_ = ["red","blue"]
num_ = ["one", "two", "three"]

se = SystemSimulator()
se.register_engine("sname", "REAL_TIME", 1)
se.get_engine("sname").insert_input_port("start")

class HumanModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name,pair):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("CREATE")
        self.insert_state("CREATE", Infinite)
        self.insert_state("WORK", 0)
        self.insert_state("CHECK",0)

        
        self.insert_input_port("info")
        self.insert_output_port("check")
        self.color__ = pair[1]
        self.num__ = pair[0]
        self.health_score = 80


    def ext_trans(self,port, msg):
        #실선
        if port == "info":
            self._cur_state = "WORK"
        elif port == "check":
            self._cur_state = "CHECK"

    def output(self):
        #점선의 레이블 현재 상태를 기반으로 어떤 데이터를 내보낼지 결정하는 역할
        self._cur_state == "CHECK"
        
        if self.color == "blue":
            print(f"?blue: {datetime.datetime.now()}")
            self.health_score += 10
            print(f"Human[{self.num__}]!blue - > rest  : health +10")
        elif self.color == "red":
            print(f"?red: {datetime.datetime.now()}")
            self.health_score -= 10
            print(f"Human[{self.num__}]red - > rest  : health -10")


        print(f"!check health: {datetime.datetime.now()}")
        if self.health_score <30:
            print(f"Humnan[{self.num__}] Health Danger!!!: {datetime.datetime.now()}")
            return None
        elif self.health_score <50:
            print(f"Humnan[{self.num__}] Health Attention: {datetime.datetime.now()}")  
            return None          
        else:
            print(f"Humnan[{self.num__}] Health is Okay: {datetime.datetime.now()}")
            return None


    def int_trans(self):
        #점선
        if self._cur_state == "WORK":
            self._cur_state = "CHECK"







class SignalGenModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("Generate", 5)
  
        self.insert_input_port("event")
        self.insert_output_port("info")
        
    def num_to_Human(self,pair):

        print("Dddddd")
        num =pair[0]
        color =pair[1]
        hm = HumanModel(0,Infinite,f"HumanModel[{num}]","sname",pair)

        #se.insert_input_port("info")
        se.register_entity(hm)
        se.coupling_relation(gen,"info",hm, "info")
        
    def ext_trans(self,port, msg):
        if port == "event":
            self._cur_state = "Generate"

                        
    def output(self):
        #print("out")
        self._cur_state == "Generate"
        color = random.choice(color_)
        num = random.choice(num_)

        print("------------------------------------")
        print(f"Detect Person Info: {num}" )
        print(f"Detect Color Info : {color}")
        print("------------------------------------")
        pair =[num,color]

        self.num_to_Human(pair)

        print(pair)

    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"


#signal generator simul engine
#se = SystemSimulator()
#se.register_engine("sname", "REAL_TIME", 1)
#se.get_engine("sname").insert_input_port("start")

gen = SignalGenModel(0, Infinite, "SignalGen", "sname")
se.get_engine("sname").register_entity(gen)


se.get_engine("sname").coupling_relation(None, "start", gen, "event")

se.get_engine("sname").insert_external_event("start", None)
se.get_engine("sname").simulate()

