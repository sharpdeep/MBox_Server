#coding=utf-8

import tornado.web
import sys
sys.path.append('..')
import setting
from core.model import User
import time

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        try:
            user = User.objects(name=username).get()
            if user.password == password:
                self.set_current_user(username)
                self.write('11')
            else:
                self.write('E01')
        except:
            self.write('E00')

    def set_current_user(self,user):
        if user:
            self.set_secure_cookie('user',tornado.escape.json_encode(user))
        else:
            self.clear_cookie('user')


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        username = self.get_current_user()
        user = User.objects(name=eval(username)).get()
        if not user.type == 'admin':
            self.render('index.html',info = 'not_admin')
        else:
            dev = user.dev
            time_t  = [time.strftime('%H:%M',time.localtime(i.makeTime)) for i in dev.temperatures]
            temp    = [i.temperature for i in dev.temperatures]
            time_h  = [time.strftime('%H:%M',time.localtime(i.makeTime)) for i in dev.humiditys]
            humi    = [i.humidity for i in dev.humiditys]
            self.render('index.html',info = zip(time_t,temp,time_h,humi),deviceId=dev.deviceId,username=username)

class AlertHandler(BaseHandler):
    """
    获取警报api
    """
    @tornado.web.authenticated
    def get(self, *params, **kwargs):
        if not len(params) == 2:
            self.write('E02')
        else:
            username,deviceId = params
            try:
                user = User.objects(name=username).get()
                dev = user.dev
                coAlert = dev.coAlert
                chAlert = dev.chAlert
                guardAlert = dev.guardAlert
                alert = map(lambda x:'1' if x else '0',[coAlert,chAlert,guardAlert])
                alert = reduce(lambda x,y:x+y,alert)
                self.write(alert)
            except:
                self.write('E00')

class TempHandler(BaseHandler):
    """
    获取温度api
    """
    @tornado.web.authenticated
    def get(self, *params, **kwargs):
        if not len(params) == 2:
            self.write('E02')
        else:
            username,deviceId = params
            try:
                user = User.objects(name=username).get()
                dev = user.dev
                temp = dev.temperatures
                temp = dict(zip([time.strftime('%m-%d %H:%M',time.localtime(i.makeTime)) for i in temp],[i.temperature for i in temp]))
                self.write(temp)
            except Exception,e:
                self.write('E00')

class HumiHandler(BaseHandler):
    """
    获取湿度api
    """
    @tornado.web.authenticated
    def get(self, *params, **kwargs):
        if not len(params) == 2:
            self.write('E02')
        else:
            username,deviceId = params
            try:
                user = User.objects(name=username).get()
                dev = user.dev
                humi = dev.humiditys
                humi = dict(zip([time.strftime('%m-%d %H:%M',time.localtime(i.makeTime)) for i in humi],[i.humidity for i in humi]))
                self.write(humi)
            except Exception,e:
                self.write('E00')
