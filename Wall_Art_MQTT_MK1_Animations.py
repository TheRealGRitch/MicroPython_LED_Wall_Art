import random
from array import *
global Hex1
global connections
from network import WLAN 
from umqtt.simple import MQTTClient
import machine, neopixel
import time



from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()





numLEDs = 120
global fade
fade = 20
global numHubs
numHubs = 7
global delay
delay = 0
global animation
animation = 14
np = neopixel.NeoPixel(machine.Pin(23), numLEDs)

Hex1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
        [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        [80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
        [90, 91, 92, 93, 94, 95, 96, 97, 98, 99],
        [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
        [110, 111, 112, 113, 114, 115, 116, 117, 118, 119]]

connections = [[1,2,3,4,5,6], #0
[0,2,6, 666,666, 666], #1
[0,1,3, 666,666, 666], #2
[0,2,4, 666,666, 666], #3
[0,3,5, 666,666, 666], #4
[0,4,6, 666,666, 666], #5
[0,5,1, 666,666, 666]] #6



def path_picker(Active_dots, life):
    i = 0
    j = 0
    count = 0
    
    path = [[666 for x in range(life)] for y in range(Active_dots)]
    
    for row in range(len(path)):
        path[row][0] = random.randint(0, numHubs-1)
        
    
    while i < Active_dots and count<50:
        while j<life-1 and count<50:
            count = count +1
            HubN = connections[path[i][j]][random.randint(0, 5)]
            if HubN != 666 and HubN not in path[i]:
                j = j+1
                path[i][j] = HubN
        
        i = i+1
        j = 0
    return path

def path_taker(path, all_rods,fade):
    #this is working as inteded. DO NOT FUCK IT UP
    #Output is:
    #[A1,B1,C1,D1,...]
    #[A2,B2,C2,D2,...]
    #.
    #.
    #.
    #[AN,BN,CN,DN,...]
    rods = [[666 for c in range(len(path[0])-1)] for r in range(len(path))]
    for i in range(len(rods)):
        for j in range(len(rods[0])):
            if path[i][j] == 0:
                if path[i][j+1] == 1:
                    rods[i][j] = [0,False]
                elif path[i][j+1] == 2:
                    rods[i][j] = [4,False]
                elif path[i][j+1] == 3:
                    rods[i][j] = [3,True]
                elif path[i][j+1] == 4:
                    rods[i][j] = [9,False]
                elif path[i][j+1] == 5:
                    rods[i][j] = [8,True]
                elif path[i][j+1] == 6:
                    rods[i][j] = [5,False]
#############################################
#############################################
                    
            if path[i][j] == 1:
                if path[i][j+1] == 0:
                    rods[i][j] = [0,True]
                elif path[i][j+1] == 2:
                    rods[i][j] = [1,False]
                elif path[i][j+1] == 6:
                    rods[i][j] = [6,True]
                    
#############################################
#############################################                    
                    
            if path[i][j] == 2:
                if path[i][j+1] == 0:
                    rods[i][j] = [4,True]
                elif path[i][j+1] == 1:
                    rods[i][j] = [1,True]
                elif path[i][j+1] == 3:
                    rods[i][j] = [2,False]
#############################################
#############################################                    
                    
            if path[i][j] == 3:
                if path[i][j+1] == 0:
                    rods[i][j] = [3,False]
                elif path[i][j+1] == 2:
                    rods[i][j] = [2,True]
                elif path[i][j+1] == 4:
                    rods[i][j] = [11,True]
#############################################
#############################################                    
                    
            if path[i][j] == 4:
                if path[i][j+1] == 0:
                    rods[i][j] = [9,True]
                elif path[i][j+1] == 3:
                    rods[i][j] = [11,False]
                elif path[i][j+1] == 5:
                    rods[i][j] = [10,False]
#############################################
#############################################                    
                    
            if path[i][j] == 5:
                if path[i][j+1] == 0:
                    rods[i][j] = [8,False]
                elif path[i][j+1] == 4:
                    rods[i][j] = [10,True]
                elif path[i][j+1] == 6:
                    rods[i][j] = [7,True]
#############################################
#############################################                    
                    
            if path[i][j] == 6:
                if path[i][j+1] == 0:
                    rods[i][j] = [5,True]
                elif path[i][j+1] == 5:
                    rods[i][j] = [7,False]
                elif path[i][j+1] == 1:
                    rods[i][j] = [6,False]
    if 666 not in rods:
        if all_rods:
            lightup_led_in_all_rods(rods, len(rods),fade)
        else:
            lightup(rods, len(rods),fade)
    else:
        print('666 in rods')


#############################################
#############################################

def lightup_led_in_all_rods(rods,dots,fade): #lights up each led in order for every rod in the paths. 
    for i in range(len(rods)):
        message_check()
        for pixel in range(len(Hex1)-1):
            for j in range(len(rods[0])-1):
                reverse = rods[i][j][1]
                n = rods[i][j][0]
                if reverse: 
                    np[Hex1[n][9-pixel]] = (255,0,0)
                        
                if not reverse:
                    np[Hex1[n][pixel-1]] = (255,0,0)
                    
            if fade ==1:
                fadeBlack(False)
            elif fade == 2:
                fadeBlack(True)
            else:
                np.write()
#############################################
#############################################
           
def lightup(rods,dots,fade):

    for j in range(len(rods[0])-1):
        message_check()
        for pixel in range(len(Hex1)-1):
            for i in range(len(rods)):
                reverse = rods[i][j][1]
                n = rods[i][j][0]
                #print(Hex1[n][pixel-1])
                if reverse: 
                    np[Hex1[n][9-pixel]] = (255,0,0)
                        
                if not reverse:
                    np[Hex1[n][pixel-1]] = (255,0,0)

                if fade ==1:
                    fadeBlack(False)
                elif fade == 2:
                    fadeBlack(True)

        
#############################################
#Animations
#############################################

def fadeBlack(empty):
    if empty:
        for a in range(numLEDs):
            i = 0
            while any(i>0 for i in np[a]):
                if np[a][i] != 0:
                    if np[a][i]>fade:
                        R = np[a][i]-fade
                    else:
                        R = np[a][0]-np[a][0]      
                    np[a] = (R,0,0)
            np.write()
    else:
        for a in range(numLEDs):
            if np[a][0] != 0:
                if np[a][0]>fade:
                    R = np[a][0]-fade
                else:
                    R = np[a][0]-np[a][0]
                np[a] = (R,0,0)
            np.write()

#############################################
#############################################
                   
def Corner_fade(fade):
    path_taker([[1,6,0],[1,2,0],[1,0,2]], False,fade)
    path_taker([[6,0,2],[6,5,0],[2,0,1],[2,3,0]], False,fade)
    path_taker([[0,4,0],[0,3,2],[3,4,0],[0,5,0],[5,4,0]],False,fade)


def rand_path(dots,life, all_rods,fade):
    procede = True
    p = path_picker(dots,life)

    for r in p:
        if 666 in r:
            procede = False
    
    if procede:
        path_taker(p, all_rods,fade)
#############################################
#############################################

#############################################
#############################################
                    
global client_id, mqtt_server, topic_sub
ssid = "******"
password = "******"
mqtt_server = '*******'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'IRremote'
topic_pub = b'Wall_Art'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


#############################################
#############################################

def sub_cb(topic, msg):
      global animation
      print(topic, msg)
      if topic == b'IRremote':
        if msg == b'0':
            animation = 0
        
        elif msg == b'1':
            animation = 1
            print(animation)
            
        elif msg == b'2':
            animation = 2
            
        elif msg == b'3':
            animation = 3
            
        elif msg == b'4':
            animation = 4
            
        elif msg == b'5':
            animation = 5
            
        elif msg == b'6':
            animation = 6
            
        elif msg == b'7':
            animation = 7
            
        elif msg == b'9':
            animation = 8
            
        elif msg == b'rew':
            animation = 9
            
        elif msg == b'info':
            animation = 10
            
        elif msg == b'page+':
            animation = 11
            
        elif msg == b'page-':
            animation = 12
            
        elif msg == b'ppv lock':
            animation = 13
            
        elif msg == b'C':
            animation = 14
            
        elif msg == b'play':
            animation = 15
            
        elif msg == b'ffwd':
            animaiton = 16
            
        elif msg == b'pause':
            animation = 17
            
        elif msg == b'stop':
            animation = 18
            
        elif msg == b'bypass':
            animation = 19
            
        elif msg == b'Tv/Vcr':
            animation = 20
        
#############################################
#############################################
 
def connect_and_subscribe():
  client =  MQTTClient(client_id, "192.168.1.31", port=1883, user=None, password=None, keepalive=30, ssl=False, ssl_params={})
  client.set_callback(sub_cb)
  client.connect(clean_session=True)
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client



def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    try:
      client.disconnect()
      time.sleep(10)
      client.connect(clean_session=True)
      print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    except OSError as e:
      time.sleep(10)
      machine.reset()

def message_check():
    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()

client = connect_and_subscribe()

#############################################
#############################################
#############################################
#############################################
#############################################
#############################################

while True:
    
    message_check()
    client.ping()
    if animation == 0:
        
        Corner_fade(1)
    elif animation == 1:
        
        rand_path(2,5,False,1)
    elif animation == 2:
        rand_path(2,5,True,1)
            
    elif animation == 3:#BURST
        path_taker([[0,1,6,0],[0,6,5,0],[0,5,4,0],[0,4,3,0],[0,3,2,0],[0,2,1,0]],False,1)
    
    elif animation == 4:#G
        path_taker([[1,6,5],[6,5,0],[5,4,3],[4,3,0],[3,2,0],[2,0,0]],True,0)
        
    elif animation == 5:#OUTER_RIM
        path_taker([[1,6,0],[6,5,0],[5,4,0],[4,3,0],[3,2,0],[2,1,0]],False,1)
        fadeBlack(True)
    elif animation == 6:#radioactive
        path_taker([[0,1,0],[1,6,0],[6,0,2],[0,5,0],[5,4,0],[4,0,4],[0,3,0],[3,2,0],[2,0,2]],True,0)
    elif animation == 7:
        print(animation)
    elif animation == 8:
        print(animation)
    elif animation == 9:
        print(animation)
    elif animation == 10:
        print(animation)
    elif animation == 11:
        print(animation)
    elif animation == 12:
        print(animation)
    elif animation == 13:
        print(animation)
    elif animation == 14:
        fadeBlack(True)
    elif animation == 15:
        print(animation)
    elif animation == 16:
        print(animation)
    elif animation == 17:
        print(animation)
    elif animation == 18:
        print(animation)
    elif animation == 19:
        print(animation)
    elif animation == 20:
        print(animation)
    #fadeBlack(True)
    #time.sleep(0.1)



