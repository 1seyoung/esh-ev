from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *
import datetime

class CommandTypeModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("S0")
        self.insert_state("S0", Infinite)
        self.insert_state("S1", 1)
        self.insert_state("S2", 1)

        self.insert_input_port("event")
        self.insert_output_port("first_cmd")
        self.insert_output_port("second_cmd")

    def ext_trans(self,port, msg):
        #실선
        if port == "event":
            print(f"?event: {datetime.datetime.now()}")
            self._cur_state = "S1"

    def output(self):
        #점선의 레이블 현재 상태를 기반으로 어떤 데이터를 내보낼지 결정하는 역할
        if self._cur_state == "S1":
            msg = SysMessage(self.get_name(), "first_cmd")
            print(f"!first command: {datetime.datetime.now()}")
            return msg
        elif self._cur_state == "S2":
            msg = SysMessage(self.get_name(), "second_cmd")
            print(f"!second command: {datetime.datetime.now()}")
            return msg
        else:
            return None

    def int_trans(self):
        #점선
        if self._cur_state == "S1":
            self._cur_state = "S2"
        elif self._cur_state == "S2":
            self._cur_state = "S0"
        else:
            self._cur_state = "S0"


# System Simulator Initialization
se = SystemSimulator()

se.register_engine("sname", "REAL_TIME", 1)

se.get_engine("sname").insert_input_port("start")

#생성시간, 소멸시간 , 모델이름 , 시뮬레이션 엔진이름
gen = CommandTypeModel(3, Infinite, "CommandType3", "sname")
se.get_engine("sname").register_entity(gen)
#start와 event연결
se.get_engine("sname").coupling_relation(None, "start", gen, "event")
print(datetime.datetime.now())
se.get_engine("sname").insert_external_event("start", None)
se.get_engine("sname").simulate()