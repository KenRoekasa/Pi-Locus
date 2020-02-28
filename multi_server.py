import socket

import draw

import json


#A function to apply trilateration formulas to return the (x,y) intersection point of three circles
def trackDevice(x1,y1,r1,x2,y2,r2,x3,y3,r3):
  A = 2*x2 - 2*x1
  B = 2*y2 - 2*y1
  C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
  D = 2*x3 - 2*x2
  E = 2*y3 - 2*y2
  F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
  x = (C*E - F*B) / (E*A - B*D)
  y = (C*D - A*F) / (B*D - A*E)
  return x,y

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        from_client = data.decode()


        datastore = json.loads(from_client)

        for addr in datastore:
            x1 = 0
            y1 = 0
            r1 = (((-datastore[addr])+27)/-24.5)*20
            x2 = 200
            y2 = 0
            r2 = 65
            x3 = 0
            y3 = 20
            r3 = 120


            
            x,y = trackDevice(x1,y1,r1,x2,y2,r2,x3,y3,r3) # change when three devices are connected
            if(addr == "C4:86:E9:19:F7:51"):
                print("Device Location of {}:".format(addr))
                print(x,y)
                draw.drawCellTowers(x1,y1,x2,y2,x3,y3,x,y)
         
        

        

        
    conn.close()
    print ('client disconnected')
    

    
