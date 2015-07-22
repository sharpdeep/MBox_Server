#coding=utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import application
from tornado.options import define,options
import sys
sys.path.append('..')
import setting


define('port',default =setting.web['port'],help = 'run on the given port',type = int)
define('ip',default=setting.web['ip'],help = 'run on the given ip', type = str)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print 'Development server is running at http://0.0.0.0:%s'% options.port
    print 'Quit the server with Ctrl+C'

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
