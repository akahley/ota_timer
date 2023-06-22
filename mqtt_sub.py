import paho.mqtt.client as paho
import sys
import os
import datetime as dt
from collections import deque
import time


global __location__
global DEVICES
start = False
reading = False
inp = ""
com_file = ""
topic_entered = False
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))



def start_reading():
    global start
    global reading
    start = True
    reading = True

def stop_reading():
    global start
    start = False

def clear_file():
    global com
    global time_stamps
    global j
    j = 0
    assert os.path.isfile(os.path.join(__location__, com_file))
    #live_coms_textbox.delete("1.0", "end") figure out how to delete the whole thing a different way


def set_mqtt_topic():
    global inp
    global topic_entered
    inp += 'topic/6D61646562796179656A61796B6179/'
    inp += input("Last 6 of serial: ")
    topic_entered = True


def define_and_create_log_file():
    global com_file
    com_file = input("File name: ")
    with open(os.path.join(__location__, com_file), 'a+') as f:
                f.write(f'{com_file}: \n')
    

delta_array = []
ota_failed_flag = 0
start_ota = deque(['10', '02', 'a3', '61'])
end_ota = deque(['10', '02', 'a3', '66'])
com = deque()
time_stamps = deque()

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    com.append(msg.payload.decode())
    time_stamps.append(dt.datetime.now().time())


client = paho.Client()
client.on_message = on_message

if client.connect("mqtt.eclipseprojects.io", 1883, 54612) != 0:
    print("Could not connect to MQTT broker")
    sys.exit(-1)

set_mqtt_topic()
#define_and_create_log_file()
start_time = dt.datetime.now().time()
end_time = start_time

client.subscribe(inp)

j=0

while(1):
    while(1):

        #### Begin Paho Reading ####

        client.loop_start()
        client.on_message
        client.loop_stop()

        ############################


        if(len(com) > 5):
            if com[0] == start_ota[0] and com[1] == start_ota[1] and com[2] == start_ota[2] and com[3] == start_ota[3]:
                start_time = time_stamps.pop()
                com.clear()
            elif com[0] == end_ota[0] and com[1] == end_ota[1] and com[2] == end_ota[2] and com[3] == end_ota[3]:
                if com[4] == '01':
                    end_time = time_stamps.pop()
                    com.clear()
                    time_stamps.clear()
                    break
                else:
                    com.clear()
                    time_stamps.clear()
                    ota_failed_flag = 1
                    break
            else:
                com.popleft()
                time_stamps.pop()

    if(not ota_failed_flag):
        delta_hour = end_time.hour - start_time.hour
        delta_minute = end_time.minute - start_time.minute
        delta_second = end_time.second - start_time.second
        delta_us = end_time.microsecond - start_time.microsecond
        print(f"{delta_hour} hours, {delta_minute} minutes, {delta_second}.{delta_us} seconds")
        break
    else:
        pass

    