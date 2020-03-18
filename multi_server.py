import socket
import sys

import draw

import json
import threading

import time as sleep

lock = threading.Lock()




stop_server = False

pos_dict = {}

def console_input():
    global stop_server
    while True:
        text_input = input("Type stop to exit!\n")
        if text_input == "stop" or text_input == "Stop":
            stop_server = True
            break


def on_new_client(clientsocket, addr):
    print('Connected to a client')
    while True:
        data = clientsocket.recv(1024)
        if not data: break
        from_client = data.decode()
        received_messages = from_client.split("|--")
        for i in range(1, len(received_messages)):
            received_data = received_messages[i].split("-|-")
            beacon_id = received_data[0]
            time = received_data[1]
            datastore = json.loads(received_data[2])
            #print("beacon:" + beacon_id + " time: " + time)



        lock.acquire()
        for blueAddr in datastore:
            #The key is the bluetooth address
            if blueAddr in pos_dict:
                pos_dict[blueAddr][beacon_id] = datastore[blueAddr]
                
            else:
                pos_dict[blueAddr] = {'1':0,'2':0,'3':0}
                pos_dict[blueAddr][beacon_id] = datastore[blueAddr]
                

        
        lock.release()

        if stop_server:
            clientsocket.close()
            break


def triangulate():
    while True:
        lock.acquire()
        #for every bluetooth address get rssi from each beacon
        for addr in pos_dict:
            x1 = 0 #x location of first beacon
            y1 = 0 #y location of first beacon
            r1 = ((pos_dict[addr]['1']+27)/-24.5)*100 #rssi value of beacon converted
            x2 = 200 #x location of second beacon
            y2 = 0 #y location of second beacon
            r2 = ((pos_dict[addr]['2']+27)/-24.5 )*100
            x3 = 0 #x location of third beacon
            y3 = 2 #y location of third beacon
            r3 = ((pos_dict[addr]['3']+27)/-24.5)*100 
            x, y = trackDevice(x1, y1, r1, x2, y2, r2, x3, y3, r3)  # change when three devices are connected
            
            if addr == "C4:86:E9:19:F7:51":
                print("Device Location of {}:".format(addr))
                print(x, y)
                draw.drawCellTowers(x1, y1, x2, y2, x3, y3, x, y,"blue")

            if addr == "F8:AD:CB:0F:D8:E6":
                print("Device Location of {}:".format(addr))
                print(x, y)
                draw.drawCellTowers(x1, y1, x2, y2, x3, y3, x, y,"red")
        lock.release()
        sleep.sleep(2)


# A function to apply trilateration formulas to return the (x,y) intersection point of three circles
def trackDevice(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    A = 2 * x2 - 2 * x1
    B = 2 * y2 - 2 * y1
    C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    D = 2 * x3 - 2 * x2
    E = 2 * y3 - 2 * y2
    F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2
    x = (C * E - F * B) / (E * A - B * D)
    y = (C * D - A * F) / (B * D - A * E)
    return x, y




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[2])
host = sys.argv[1]
sock.bind((host, port))
sock.listen(5)
print('Started Server')
y = threading.Thread(target=console_input)
print("starting console input thread")
y.start()
z = threading.Thread(target=triangulate)
print("starting triangulate thread")
z.start()

while True:
    conn, addr = sock.accept()
    x = threading.Thread(target=on_new_client, args=(conn, addr))
    x.start()
   
sock.close()
print('server disconnected')
