#coding=utf-8

import tornado.web
import sys
sys.path.append('..')
import setting
from core.model import User

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user')

class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument("username")
        password = self.get_argument("password")

        try:
            user = User.objects(name=username).get()
        except:
            
