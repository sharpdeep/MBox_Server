#coding=utf-8

import logging
from logging.handlers import RotatingFileHandler
from gevent.server import StreamServer
from gevent import monkey
from gevent import Greenlet
import gevent
from gevent import socket
from handler import DeviceConnect,DeviceTerminal,DeviceSocketSend
monkey.patch_socket()
import sys
sys.path.append('..')
import setting
import time
from core import unpack
from core.model import Device,Temperature,Humidity

"""
上传数据:温度+湿度
"""
def postData(sock,deviceId,params):
    sock.send('I got it\n')
    if not len(params) == setting.device['postNum']:
        sock.send('param num error!')
        return None
    try:
        device = Device.objects(deviceId=deviceId).get()
    except:
        sock.send('register first')
        return None
    device.temperatures.append(Temperature(temperature=eval(params[0]),makeTime=time.time()))
    device.humiditys.append(Humidity(humidity=eval(params[1]),makeTime=time.time()))
    device.lastTime = time.time()
    device.save()
    sock.send('ok')

def sos(sock,deviceId,params):
    sock.send('I got it\n')
    if not len(params) == setting.device['sosNum']:
        sock.send('params num error')
        return None
    try:
        device = Device.objects(deviceId=deviceId).get()
    except:
        sock.send('register first')
        return None
    device.coAlert = eval(params[0])
    device.chAlert = eval(params[1])
    device.guardAlert = eval(params[2])
    device.lastTime = time.time()
    device.save()
    sock.send('ok')
    """
    此处应有推送
    """

def register(sock,deviceId,params):
    try:
        Device(deviceId=deviceId)
        sock.send('register ok')
    except:
        sock.send('register faild')

def sendtodev(sock,deviceId,params):
    if deviceId in DeviceList:
        if not DeviceList[deviceId].conn:
            sock.sendall('no1')
            return None
        DeviceList[deviceId].conn.send(deviceId,params[0],params[1:])
        sock.sendall('ok')
    else:
        sock.sendall('no2')

def timeLiving(dt):
    while True:
        gevent.sleep(10)
        device = Device.objects(deviceId=dt.deviceId).get()
        if time.time() - device.lastTime > setting.server['living']:    # 2分钟未更新数据视为断线
            dt.conn.stop()
            del DeviceList[dt.deviceId]
            return None



DeviceList = {}
ComandList = {
    'post'      :   postData,
    'sos'       :   sos,
    'register'  :   register,
    'sendtodev' :   sendtodev,
}

def handle(sock,addr):
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)

    deviceId,command,params = unpack.read(sock)
    try:
        Device.objects(deviceId=deviceId).get()
    except:
        sock.send('register first!')
        return None
    """
    短连接命令执行
    """
    if command in ComandList:
        ComandList[command](sock,deviceId,params)
        return None
    # 建立长连接
    elif command == 'conn':
        dc = DeviceConnect(sock,addr)
        if not deviceId in DeviceList:
            dt = DeviceTerminal(deviceId)
            a = Greenlet.spawn(timeLiving,dt)
            a.start()
            DeviceList[deviceId] = dt
        else:
            dt = DeviceList[deviceId]
            if dt.conn:
                dt.conn.stop()
        dt.connect(dc)
        # 循环发送队列消息
        a = Greenlet.spawn(DeviceSocketSend,dt,dc)
        a.start()

logger = logging.getLogger('server')
logfile = setting.server['logfile']
File_logging = RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=50)
File_logging.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
File_logging.setLevel(setting.server['loglevel'])
logger.addHandler(File_logging)
logger.setLevel(setting.server['loglevel'])


if __name__ == "__main__":
    print('Hello')
    StreamServer(('',setting.server['port']),handle).serve_forever()