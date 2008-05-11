import types
import logging
from django.utils import simplejson
from birdnest.filter import Filter

class StatusesIncludeImage(Filter):
  def filter(self, text):
    unwanted_status = ['truncated', 'in_reply_to_user_id',
                       'in_reply_to_status_id', 'favorited']
    unwanted_user = ['description', 'followers_count', 'protected',
                     'location']
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
                     'location', 'profile_image_url']
    statuses = simplejson.loads(text)
    for status in statuses:
      for key in unwanted_status:
        del status[key]
      for key in unwanted_user:
        del status['user'][key]
    return simplejson.dumps(statuses)

class SingleStatusesIncludeImage(Filter):
  def filter(self, text):
    unwanted_status = ['truncated', 'in_reply_to_user_id',
                       'in_reply_to_status_id', 'favorited']
    unwanted_user = ['description', 'followers_count', 'protected',
                     'location']
    status = simplejson.loads(text)
    logging.info(status)
    for key in unwanted_status:
      del status[key]
    for key in unwanted_user:
      del status['user'][key]
    return simplejson.dumps(status)

class SingleStatusesTextOnly(Filter):
  def filter(self, text):
    unwanted_status = ['truncated', 'in_reply_to_user_id',
                       'in_reply_to_status_id', 'favorited']
    unwanted_user = ['description', 'followers_count', 'protected',
                     'location', 'profile_image_url']
    status = simplejson.loads(text)
    for key in unwanted_status:
      del status[key]
    for key in unwanted_user:
      del status['user'][key]
    return simplejson.dumps(status)

class DirectMessageIncludeImage(Filter):
  def filter(self, text):
    directmessages = simplejson.loads(text)
    for dm in directmessages:
      sender = dm['sender']
      recipient = dm['recipient']
      dm['sender']  = dm['recipient'] = {}
      dm['sender']['profile_image_url'] = sender['profile_image_url']
      dm['recipient']['profile_image_url'] = recipient['profile_image_url']
    return simplejson.dumps(directmessages)

class DirectMessageTextOnly(Filter):
  def filter(self, text):
    unwanted_dm = ['sender', 'recipient']
    directmessages = simplejson.loads(text)
    for dm in directmessages:
      for key in unwanted_dm:
        del dm[key]
    return simplejson.dumps(directmessages)

class SingleDirectMessageIncludeImage(Filter):
  def filter(self, text):
    dm = simplejson.loads(text)
    sender = dm['sender']
    recipient = dm['recipient']
    dm['sender']  = dm['recipient'] = {}
    dm['sender']['profile_image_url'] = sender['profile_image_url']
    dm['recipient']['profile_image_url'] = recipient['profile_image_url']
    return simplejson.dumps(dm)


class SingleDirectMessageTextOnly(Filter):
  def filter(self, text):
    unwanted_dm = ['sender', 'recipient']
    dm = simplejson.loads(text)
    for key in unwanted_dm:
        del dm[key]
    return simplejson.dumps(dm)