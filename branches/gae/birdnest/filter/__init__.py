import re

class Filter(object):
  def filter(self, text):
    return text

  def error_reason(self, text, reason):
    return reason

  def error_filter(self, text):
    return text

def remove_html(text):
  return re.sub(r'<.*?>', '', text)
