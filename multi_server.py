import socket
import sys

import draw

import json
import threading

import time as sleep


stop_server = False

pos_dict = {}

def console_input():
    global stop_server
    while True:
        text_input = input("Type stop to exit!\n")
        if text_input == "stop" or text_input == "Stop":
            stop_server = True


def on_new_client(clientsocket, addr):
    print('Connected to a client')
    while True:
        data = clientsocket.recv(1024)
        if not data: break
        from_client = data.decode()
        received_data = from_client.split("-|-")
        beacon_id = received_data[0]
        time = received_data[1]
        datastore = json.loads(received_data[2])




        for addr in pos_dict:
            pos_dict[addr][int(beacon_id)-1] = (((-datastore[addr]) + 27) / -24.5) * 20





        if stop_server:
            break
    clientsocket.close()
    sys.exit(0)


def triangulate():
    while True:
            x1 = 0
            y1 = 0
            r1 = pos_dict[addr][0]
            x2 = 200
            y2 = 0
            r2 = pos_dict[addr][1]
            x3 = 0
            y3 = 20
            r3 = pos_dict[addr][2]

            x, y = trackDevice(x1, y1, r1, x2, y2, r2, x3, y3, r3)  # change when three devices are connected
            if addr == "C4:86:E9:19:F7:51" or addr == "F8:AD:CB:0F:D8:E6":
                print("Device Location of {}:".format(addr))
                print(x, y)
                draw.drawCellTowers(x1, y1, x2, y2, x3, y3, x, y)
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
port = 8080
host = 'localhost'
sock.bind((host, port))
sock.listen(5)
print('Started Server')

while True:
    conn, addr = sock.accept()
    x = threading.Thread(target=on_new_client, args=(conn, addr))
    x.start()
    y = threading.Thread(target=console_input)
    y.start()
sock.close()
print('server disconnected')
