#coding=utf-8

from url import url

import tornado.web
import os
import base64,uuid

secretKey = base64.b64encode(uuid.uuid4().bytes+uuid.uuid4().bytes)

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__),'templates'),
    static_path = os.path.join(os.path.dirname(__file__),'statics'),
    cookie_secret = secretKey,#cookie“加密”
    login_url = '/login',#如果当前用户没登录，会找到该目录
    debug = True,
    )

application = tornado.web.Application(
    handlers = url,
    **settings
    )
