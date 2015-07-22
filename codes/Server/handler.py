#coding = utf-8
import gevent
from gevent import queue
import sys
sys.path.append('..')
from core.model import Device

def DeviceSocketSend(dt,dc):
    gevent.sleep(10)
    if not dt.conn is dc:
        dc.stop()
        return None
    try:
        while dc.status:
            data = dc.send_Q.get()
            dc.sock.sendall(data)
            gevent.sleep(1)
    except:
        dt.disconnect(dc)
        print('error')
        return None


class DeviceTerminal(object):

    def __init__(self,deviceId):
        self.deviceId = deviceId
        try:
            dev = Device.objects(deviceId=deviceId).get()
        except:
            dev = Device(deviceId=deviceId)
            dev.save()
        self.dev = dev

    def connect(self,dc):
        self.conn = dc
        dc.dev = self

    def disconnect(self,dc):
        if dc is self.conn:
            self.conn = None

class DeviceConnect(object):

    def __init__(self,sock,addr):
        self.sock = sock
        self.addr = addr
        self.status = True
        self.send_Q = queue.Queue()
        self.recv_Q = queue.Queue()


    def stop(self):
        self.status = False
        self.dev.disconnect(self)
        self.sock.close()

    def send(self,deviceId,command,params):
        params = map(lambda x:str(x),params)
        self.send_Q.put('['+','.join([deviceId,command,'|'.join(params)])+']')

    def recv(self,data):
        self.recv_Q.put(data)




