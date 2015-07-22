#coding = utf-8

import socket

def read(sock):
    d = sock.recv(1)
    if d:
        if d=='[':
            k = 0
            deviceId = ''
            command = ''
            params = []
            temp = ''
            while True:
                d = sock.recv(1)
                if not d:
                    break
                if d == ',':
                    k += 1
                    d = ''
                else:
                    if d == ']':
                        break
                    if k == 0:
                        deviceId += d
                    if k == 1:
                        command += d
                    if k == 2:
                        temp += d
            if d == ']':
                params = temp.split('|')
            return deviceId,command,params
        else:
            return None,None,None
    else:
        return None,None,None