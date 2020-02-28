import socket

import draw

import json
import threading

stop_server = False


def console_input():
    global stop_server
    while True:
        text_input = input("Type stop to exit!\n")
        if text_input == "stop" or text_input == "Stop":
            stop_server = True;


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

        for addr in datastore:
            x1 = 0
            y1 = 0
            r1 = (((-datastore[addr]) + 27) / -24.5) * 20
            x2 = 200
            y2 = 0
            r2 = 65
            x3 = 0
            y3 = 20
            r3 = 120

            x, y = trackDevice(x1, y1, r1, x2, y2, r2, x3, y3, r3)  # change when three devices are connected
            if addr == "C4:86:E9:19:F7:51":
                print("Device Location of {}:".format(addr))
                print(x, y)
                draw.drawCellTowers(x1, y1, x2, y2, x3, y3, x, y)

        if stop_server:
            break
    clientsocket.close()




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
sock.close()
print('server disconnected')
