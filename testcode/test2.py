from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

import datetime

class PEG(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)

        self.insert_input_port("start")
        self.insert_output_port("process")

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"[{self.get_name()}][IN]: {datetime.datetime.now()}")
            self._cur_state = "Generate"

    def output(self):
        msg = SysMessage(self.get_name(), "process")
        msg.insert(f"[{self.get_name()}][OUT]: {datetime.datetime.now()}")
        return msg
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

class MsgRecv(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)

        self.insert_input_port("recv")

    def ext_trans(self,port, msg):
        if port == "recv":
            data = msg.retrieve()
            print("text processing", data)
            self._cur_state = "Wait"

    def output(self):
        return None
    
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"

class MsgRecv2(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)

        self.insert_input_port("recv")

    def ext_trans(self,port, msg):
        if port == "recv":
            data = msg.retrieve()
            print("image processing", data)
            self._cur_state = "Wait"

    def output(self):
        return None
        
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"

ss = SystemSimulator()
ss.register_engine("simple", "REAL_TIME", 1)
ss.get_engine("simple").insert_input_port("start")

gen = PEG(0, Infinite, f"Gen", "simple")
ss.get_engine("simple").register_entity(gen)
ss.get_engine("simple").coupling_relation(None, "start", gen, "start")

proc = MsgRecv(0, Infinite, f"Proc", "simple")
ss.get_engine("simple").register_entity(proc)
ss.get_engine("simple").coupling_relation(gen, "process", proc, "recv")

proc2 = MsgRecv2(0, Infinite, f"Proc2", "simple")
ss.get_engine("simple").register_entity(proc2)
ss.get_engine("simple").coupling_relation(gen, "process", proc2, "recv")

ss.get_engine("simple").insert_external_event("start", None)
ss.get_engine("simple").simulate()

