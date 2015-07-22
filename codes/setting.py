#coding=utf-8
import logging

server = {
    'port'      :   8080,
    'buffSize'  :   1024,
    'logfile'   :   './server.log',
    'loglevel'  :   logging.INFO,
    'living'    :   120,
}

web = {
    'port'      :   8090,
    'ip'        :   '0.0.0.0'
}

db = {
    'name'      :   'MBox'
}

device = {
    'postNum'   :   2,  # 温度、湿度
    'sosNum'    :   3,
}