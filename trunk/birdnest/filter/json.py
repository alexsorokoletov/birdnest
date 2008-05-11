import types

from django.utils import simplejson
from birdnest.filter import Filter

class StatusesIncludeImage(Filter):
  def filter(self, text):
    unwanted_status = ['truncated', 'in_reply_to_user_id',
                       'in_reply_to_status_id', 'favorited']
    unwanted_user = ['description', 'followers_count', 'protected']
    statuses = simplejson.loads(text)
    for status in statuses:
      for key in unwanted_status:
        del status[key]
      for key in unwanted_user:
        del status['user'][key]
    return simplejson.dumps(statuses)

class StatusesTextOnly(Filter):
  def filter(self, text):
    unwanted_status = ['truncated', 'in_reply_to_user_id',
                       'in_reply_to_status_id', 'favorited']
    unwanted_user = ['description', 'followers_count', 'protected',
                     'profile_image_url']
    statuses = simplejson.loads(text)
    for status in statuses:
      for key in unwanted_status:
        del status[key]
      for key in unwanted_user:
        del status['user'][key]
    return simplejson.dumps(statuses)
