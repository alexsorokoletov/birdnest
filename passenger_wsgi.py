import os, sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "nest"))
sys.path.insert(0, path)
#import web
#import nest.code
#application = web.application(nest.code.urls, globals()).wsgifunc()
import socket
#ua = os.environ.get("HTTP_USER_AGENT", "")
#if ua.find('jibjib') >= 0:
#  socket.setdefaulttimeout(15)
#elif ua.find('zh-CN') >= 0:
#  sys.exit(0)
#else:
#  socket.setdefaulttimeout(2)
socket.setdefaulttimeout(60)
import code
code.init_logger(os.path.dirname(__file__))
app = code.app
application = code.application
