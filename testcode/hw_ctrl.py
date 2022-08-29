from system_simulator import SystemSimulator
from behavior_model_executor import BehaviorModelExecutor
from system_message import SysMessage
from definition import *

import socket
import threading
import time
import datetime


from telegram.ext import Updater, CommandHandler

import zmq
class ZMQHandler:
    def __init__(self, ip='', port=5555):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")
        
    def send_command(self, command):
        self.socket.send(command.encode('utf-8'))

class TelloModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, tello_handler):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)

        self.insert_input_port("cmd")

        self.cmd_list = []
        self.th = tello_handler

    def ext_trans(self,port, msg):
        if port == "cmd":
            print(f"[Tello][IN]: {datetime.datetime.now()}")
            self.cancel_rescheduling()

            data = msg.retrieve()
            self.cmd_list.append(data[0])
            self._cur_state = "PROCESS"

    def output(self):
        print(f"[Tello][Send]: {datetime.datetime.now()}")
        print(self.cmd_list)
        self.th.send_command(self.cmd_list[0])
        self.cmd_list = []
        return None

    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
        else:
            self._cur_state = "IDLE"

# System Simulator Initialization
ss = SystemSimulator()
ss.register_engine("sname", "REAL_TIME", 0.01)

#print("DD")
ss.exec_non_block_simulate(["sname"])
#teh = TelloNetworkEventHandler()
teh = ZMQHandler()

#se.get_engine("sname2").insert_external_event("start", None)

def cmd_helper(cmd, comment):
    return f"/{cmd}: {comment}"
##
def cmd_handler_helper(cmd, sim_engine):

    tm = TelloModel(0, Infinite, f"Tello[{cmd}]", "sname", teh)

    sim_engine.insert_input_port(cmd)
    sim_engine.register_entity(tm)
    sim_engine.coupling_relation(None, f"{cmd}", tm, "cmd")
    
    def func(update, context):
        print(update.message.text)
        sim_engine.insert_external_event(f"{cmd}", update.message.text[1:])
        ####추가할 수 도 있고 있다고 가정하고 모델한테 내용을 넣어도 괜찮음
        ###83 - 외부 인터페이스와 시뮬레이션 엔진의 접점/// 외부 엔진에서 포트
        ##77 - 엔진에 포트가 추가하고있어야함
        ##78- 이벤트를 받을(처리할) 모델이 추가되어야함
        ##79- 엔진에 추가한 포트와 이벤트를 처리할 포트의 모델과 연결시켜야함
        ### 789 선행(시뮬레이션을 위해 소프트웨어를 초기화 역할) ->83 가능(비동기방식으로 동작하다가 이벤트가 생성되면 초기화된 규칙에 맞춰 해당하는 모델에 전송)
        ### 789, 81, 83  = 필요한이유? : 귀찮아서(커맨드처리하는거 앞에 커맨드 + arg=> 처리구조가 다 똑같음(/command arg ~) 앞에 슬래쉬만 날리고 뒤에만 살리면 처리가능)=>일련의 과정을 자동화 시킨 것 (커맨드가 생길때마다 양이 늘어나는 것을 방지할 수 있음)
        ### 함수 오브젝트 자동 생성
        ### 휴맨모델을 생성해서 연결시키면됨(해야하는 것)
        ### 73 함수 활용한다고 하면 fun 은 사라지고(왜냐면 텔레그램 처리를 위해서 만든것이기때문에(커맨드 핸들라가 호출되었을때 함수 생성하는- 109line)) 사람이 오면 등록하고 (register_entity) 후 이벤트 연결 
    return func
###
def help(update, context):
    l_menu = ["Tello Control Menu", cmd_helper("takeoff"), cmd_helper("/land")]
    update.message.reply_text("\n".join(l_menu))

command_list = ["takeoff", "land","flip"]

updater = Updater("5571793758:AAHOh26UHtHLF4rO9_hZ1qIuKADJkrlUetw", use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

for cmd in command_list:
    chh = cmd_handler_helper(cmd, ss.get_engine("sname"))
    dp.add_handler(CommandHandler(cmd, chh))

# Start the Bot
updater.start_polling()

import signal
import sys

def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    updater.shutdown()
    del ss
    sys.exit(0)

signal.signal(signal.SIGINT, sigterm_handler)
signal.signal(signal.SIGTERM, sigterm_handler)

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()