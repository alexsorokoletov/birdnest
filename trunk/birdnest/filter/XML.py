import types
import logging
from xml.etree import ElementTree as ET
from birdnest.filter import Filter

def copy_element(builder, source, tag):
  builder.start(tag, {})
  builder.data(source.findtext(tag))
  builder.end(tag)

class StatusesIncludeImage(Filter):
  def filter(self, text):
    wanted_status = ['created_at', 'id', 'text', 'source']
    wanted_user = ['id', 'name', 'screen_name', 'profile_image_url', 'url']
    root = ET.fromstring(text)
    builder = ET.TreeBuilder()
    builder.start('statuses', {'type': 'array'})
    for status in root.findall('status'):
      builder.start('status', {})
      for tag in wanted_status:
        copy_element(builder, status, tag)

      user = status.find('user')
      builder.start('user', {})
      for tag in wanted_user:
        copy_element(builder, user, tag)
      builder.end('user')

      builder.end('status')
    builder.end('statuses')
    return ET.tostring(builder.close())

class StatusesTextOnly(Filter):
  def filter(self, text):
    wanted_status = ['created_at', 'id', 'text', 'source']
    wanted_user = ['id', 'name', 'screen_name', 'url']
    root = ET.fromstring(text)
    builder = ET.TreeBuilder()
    builder.start('statuses', {'type': 'array'})
    for status in root.findall('status'):
      builder.start('status', {})
      for tag in wanted_status:
        copy_element(builder, status, tag)

      user = status.find('user')
      builder.start('user', {})
      for tag in wanted_user:
        copy_element(builder, user, tag)
      builder.end('user')

      builder.end('status')
    builder.end('statuses')
    return ET.tostring(builder.close(), 'UTF-8')

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
