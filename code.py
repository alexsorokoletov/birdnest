import wsgiref.handlers
import logging
import traceback
from google.appengine.api import urlfetch
from google.appengine.ext import webapp

from birdnest import filter
from birdnest.filter import json
from birdnest.filter import XML

twitterAPI = "http://twitter.com/"

class BaseProxy(webapp.RequestHandler):

  required_header = ['Authorization',
                     'User-Agent',
                     'X-Twitter-Client',
                     'X-Twitter-Client-URL',
                     'X-Twitter-Client-Version']

  def __init__(self):
    pass

  def _get_headers(self):
    headers = {}
    for header in self.required_header:
      if self.request.headers.has_key(header):
        headers[header] = self.request.headers[header]
    return headers

  def get(self, params):    
    result = None
    url = twitterAPI + params
    headers = self._get_headers()

    try:
      for i in range(2):
        try:
          result = urlfetch.fetch(url, headers=headers)
          self.sendoutput(result)
          break
        except urlfetch.DownloadError, why:
          pass
      if not result:
        raise urlfetch.DownloadError()
    except urlfetch.InvalidURLError, why:
      self.error(400)
      logging.error("InvalidURLError %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except urlfetch.DownloadError, why:
      self.error(504)
      logging.error("DownloadError %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except urlfetch.ResponseTooLargeError, why:
      self.error(413)
      logging.error("ResponseTooLargeError %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except urlfetch.Error, why:
      self.error(502)
      logging.error("urlfetch.Error %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except Exception, inst:
      self.error(500)
      if result:
        logging.error("%s \n\n %s \n\n %s \n\n %s \n\n %s" % (url, str(inst), self.request.headers, self.request.body.decode('latin-1'), result.content.decode('latin-1')))
      else:
        logging.error("%s \n\n %s \n\n %s \n\n %s" % (url, str(inst), self.request.headers, self.request.body.decode('latin-1')))

  def sendoutput(self, result):
    if result.status_code == 200:
      self.response.headers = result.headers
      if len(result.content.strip()) > 0:
        self.response.out.write(self.filter(result.content))
    else:
      self.error(result.status_code)
      self.response.out.write(result.content)

  def post(self, params):
    result = None
    url = twitterAPI + params
    headers = self._get_headers()

    try:
      result = urlfetch.fetch(url, payload=self.request.body, method=urlfetch.POST, headers=headers)
      self.sendoutput(result)
    except urlfetch.InvalidURLError, why:
      self.error(400)
      logging.error("InvalidURLError %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except urlfetch.DownloadError, why:
      self.error(504)
      logging.error("DownloadError %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except urlfetch.ResponseTooLargeError, why:
      self.error(413)
      logging.error("ResponseTooLargeError %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except urlfetch.Error, why:
      self.error(502)
      logging.error("urlfetch.Error %s", url)
      logging.error("%s" % self.request.headers)
      logging.error("%s" % self.request.body.decode('latin-1'))
    except Exception, inst:
      self.error(500)
      if result:
        logging.error("%s \n\n %s \n\n %s \n\n %s \n\n %s" % (url, str(inst), self.request.headers, self.request.body.decode('latin-1'), result.content.decode('latin-1')))
      else:
        logging.error("%s \n\n %s \n\n %s \n\n %s" % (url, str(inst), self.request.headers, self.request.body.decode('latin-1')))

class OptimizedProxy(BaseProxy):

  user_agent = None

  def __init__(self):
    BaseProxy.__init__(self)

  def _get_headers(self):
    headers = BaseProxy._get_headers(self)
    if self.user_agent:
      headers['User-Agent'] = self.user_agent
    return headers

  def sendoutput(self, result):
    if result.status_code == 200:
      self.response.headers = result.headers
      if len(result.content.strip()) > 0:
        self.response.out.write(self.filter(result.content))
    elif result.status_code == 304:
      self.response.headers = result.headers
    else:
      self.error(result.status_code)
      self.response.out.write('')
    
class NoFilterProxy(BaseProxy, filter.Filter):
  pass

class NoFilterOptimizedProxy(OptimizedProxy, filter.Filter):
  pass

class JSONStatusesIncludeImageProxy(OptimizedProxy, json.StatusesIncludeImage):
  pass

class JSONStatusesTextOnlyProxy(OptimizedProxy, json.StatusesTextOnly):
  pass

class JSONSingleStatusesIncludeImageProxy(OptimizedProxy, json.SingleStatusesIncludeImage):
  pass

class JSONSingleStatusesTextOnlyProxy(OptimizedProxy, json.SingleStatusesTextOnly):
  pass


class JSONDirectMessageTextOnlyProxy(OptimizedProxy, json.DirectMessageTextOnly):
  pass

class JSONDirectMessageIncludeImageProxy(OptimizedProxy, json.DirectMessageIncludeImage):
  pass

class JSONSingleDirectMessageTextOnlyProxy(OptimizedProxy, json.SingleDirectMessageTextOnly):
  pass

class JSONSingleDirectMessageIncludeImageProxy(OptimizedProxy, json.SingleDirectMessageIncludeImage):
  pass

class XMLStatusesIncludeImageProxy(OptimizedProxy, XML.StatusesIncludeImage):
  pass

class XMLStatusesTextOnlyProxy(OptimizedProxy, XML.StatusesTextOnly):
  pass

def main():
  application = webapp.WSGIApplication([
    ('/api/(.*)', NoFilterProxy),

    ('/optimized/(.*)', NoFilterOptimizedProxy),

    ('/text/(statuses/public_timeline\.json)', JSONStatusesTextOnlyProxy),
    ('/text/(statuses/public_timeline\.xml)', XMLStatusesTextOnlyProxy),
    ('/text/(statuses/user_timeline\.json)', JSONStatusesTextOnlyProxy),
    ('/text/(statuses/user_timeline\.xml)', XMLStatusesTextOnlyProxy),
    ('/text/(statuses/friends_timeline\.json)', JSONStatusesTextOnlyProxy),
    ('/text/(statuses/friends_timeline\.xml)', XMLStatusesTextOnlyProxy),
    ('/text/(statuses/replies\.json)', JSONStatusesTextOnlyProxy),
    ('/text/(statuses/replies\.xml)', XMLStatusesTextOnlyProxy),
    ('/text/(statuses/update\.json)', JSONSingleStatusesTextOnlyProxy),
    ('/text/(direct_messages\.json)', JSONDirectMessageTextOnlyProxy),
    ('/text/(direct_messages/sent\.json)', JSONDirectMessageTextOnlyProxy),
    ('/text/(direct_messages/new\.json)', JSONSingleDirectMessageTextOnlyProxy),
    ('/text/(direct_messages/delete/\d+\.json)', JSONSingleDirectMessageTextOnlyProxy),
    ('/text/(.*)', NoFilterOptimizedProxy),

    ('/image/(statuses/public_timeline\.json)', JSONStatusesIncludeImageProxy),
    ('/image/(statuses/public_timeline\.xml)', XMLStatusesIncludeImageProxy),
    ('/image/(statuses/user_timeline\.json)', JSONStatusesIncludeImageProxy),
    ('/image/(statuses/user_timeline\.xml)', XMLStatusesIncludeImageProxy),
    ('/image/(statuses/friends_timeline\.json)', JSONStatusesIncludeImageProxy),
    ('/image/(statuses/friends_timeline\.xml)', XMLStatusesIncludeImageProxy),
    ('/image/(statuses/replies\.json)', JSONStatusesIncludeImageProxy),
    ('/image/(statuses/replies\.xml)', XMLStatusesIncludeImageProxy),
    ('/image/(statuses/update\.json)', JSONSingleStatusesIncludeImageProxy),
    ('/image/(direct_messages\.json)', JSONDirectMessageIncludeImageProxy),
    ('/image/(direct_messages/sent\.json)', JSONDirectMessageIncludeImageProxy),
    ('/image/(direct_messages/new\.json)', JSONSingleDirectMessageIncludeImageProxy),
    ('/image/(direct_messages/delete/\d+\.json)', JSONSingleDirectMessageIncludeImageProxy),
    ('/image/(.*)', NoFilterOptimizedProxy)],
    debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
