import struct
import sys


import bluetooth
import bluetooth._bluetooth as bluez  # low level bluetooth wrappers

import json


import socket


def connect(sock):
    ip = 'localhost'
    port = 8080
    sock.connect((ip, port))


def sendJson(jsonString):
    WIFI_sock.send(jsonString)



def setup_server(serv):
    ip = 'localhost'
    port = 8080
    serv.bind((ip, port))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_client = ''
        while True:
            data = conn.recv(4096)
            if not data: break
            from_client += data
            print (from_client)
            conn.send("I am SERVER<br>")
        conn.close()
        print ('client disconnected')


def read_inquiry_mode(sock):
    """returns the current mode, or -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # read_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL,
                                   bluez.OCF_READ_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE)
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

    # first read the current inquiry mode.
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL,
                       bluez.OCF_READ_INQUIRY_MODE)

    pkt = sock.recv(255)
    status, mode = struct.unpack("xxxxxxBB", pkt)

    # restore old filter
    sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter)

    return mode


def device_inquiry_with_with_rssi(sock):
    # save current filter
    old_filter = sock.getsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, flt)

    duration = 2
    max_responses = 255
    cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
    bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

    results = {}

    while True:
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        print("Event: {}".format(event))
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            pkt = pkt[3:]
            nrsp = bluetooth.get_byte(pkt[0])
            for i in range(nrsp):
                addr = bluez.ba2str(pkt[1+6*i:1+6*i+6])
                rssi = bluetooth.byte_to_signed_int(
                    bluetooth.get_byte(pkt[1 + 13 * nrsp + i]))
                #Add addr and rssi to map
                results[addr] = rssi
                print("[{}] RSSI: {}".format(addr, rssi))
        elif event == bluez.EVT_INQUIRY_COMPLETE:
            break
        elif event == bluez.EVT_CMD_STATUS:
            status, ncmd, opcode = struct.unpack("BBH", pkt[3:7])
            if status:
                print("Uh oh...")
                printpacket(pkt[3:7])
                break
        elif event == bluez.EVT_INQUIRY_RESULT:
            pkt = pkt[3:]
            nrsp = bluetooth.get_byte(pkt[0])
            for i in range(nrsp):
                addr = bluez.ba2str(pkt[1+6*i:1+6*i+6])
                results[addr] = -1
                print("[{}] (no RRSI)".format(addr))
                
        else:
            print("Unrecognized packet type 0x{:02x}.".format(ptype))

    # restore old filter
    sock.setsockopt(bluez.SOL_HCI, bluez.HCI_FILTER, old_filter)

    return results




def convert_to_JSON(datastore):
    json_string = json.dumps(datastore)
    return json_string


    
def convert_from_JSON(jsonString):
    datastore= json.loads(jsonString)













dev_id = 0
try:
    # Create raw HCI sock to set our BT name
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Error accessing bluetooth device.")
    sys.exit(1)

#Test if you can read from it
try:
    mode = read_inquiry_mode(sock)
except Exception as e:
    print("Error reading inquiry mode.")
    print("Are you sure this a bluetooth 1.2 device?")
    print(e)
    sys.exit(1)
print("Current inquiry mode is", mode)

WIFI_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connect(WIFI_sock)


for i in range(0,50):
    rssiResults = device_inquiry_with_with_rssi(sock)
    if rssiResults != {}:
        WIFI_sock.send(convert_to_JSON(rssiResults).encode())
WIFI_sock.close()





