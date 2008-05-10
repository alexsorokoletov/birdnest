import wsgiref.handlers
import logging
from google.appengine.api import urlfetch
from google.appengine.ext import webapp

twitterAPI = "http://twitter.com/"

class Filter():
  def filter(self, returnText, method):
    pass

class IncludeImageFilter(Filter):
  def filter(self, returnText, method):
    pass

class TextOnlyFilter(IncludeImageFilter):
  def filter(self, returnText, method):
    pass

class BaseProxy(webapp.RequestHandler):
  def __init__(self):
    self.filter = Filter()
    self.required_header = ['Authorization', 'User-Agent', 'X-Twitter-Client', 'X-Twitter-Client-URL', 'X-Twitter-Client-Version']

  def get(self, params):    
    url = twitterAPI + params
    headers = {}
    for header in self.required_header:
      if self.request.headers.has_key(header):
        headers[header] = self.request.headers[header]

    result = urlfetch.fetch(url, headers=headers)
    self.sendoutput(result)

  def sendoutput(self, result):
    if result.status_code == 200:
      self.response.headers = result.headers
      self.response.out.write(result.content)
    else:
      self.error(result.status_code)
      self.response.out.write(result.content)
    
    
  def post(self, params):
    url = twitterAPI + params
    headers = {}
    for header in self.required_header:
      if self.request.headers.has_key(header):
        headers[header] = self.request.headers[header]
    try:
      result = urlfetch.fetch(url, payload=self.request.body, method=urlfetch.POST, headers=headers)
      self.sendoutput(result)
    except Exception, inst:
        self.error(500)
        logging.error("%s \n\n %s \n\n %s " % ( inst, self.request.headers, self.request.body))

class OptimizedProxy(BaseProxy):
  def __init__(self):
    self.filter = OptimizedFilter()

  def sendoutput(self, result):
    if result.status_code == 200:
      self.response.headers = result.headers
      self.response.out.write(result.content)
    else:
      self.error(result.status_code)
      self.response.out.write('')
    
class TextOnlyProxy(Optimizedy):
  def __init__(self):
    self.filter = TextOnlyFilter()

class IncludeImageProxy(Optimizedy):
  def __init__(self):
    self.filter = IncludeImageFilter()

def main():
  application = webapp.WSGIApplication(
                                       [('/api/(.*)', BaseProxy),
                                       ('/optimized/(.*)', OptimizedProxy),
                                       ('/text/(.*)', TextOnlyProxy),
                                       ('/image/(.*)', IncludeImageProxy)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
