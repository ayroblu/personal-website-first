import datetime
from google.appengine.ext import db

class Log(db.Model):
	#name = db.StringProperty(required=True) # called with users.get_current_user().name()
	ip = db.StringProperty(required=True)
	timedate = db.DateTimeProperty(auto_now_add=True)
	message = db.StringProperty(required=True)
    
def getLogs(start, num):
    q = db.Query(Log)
    q = q.order('-timedate')
    return q.fetch(limit=num,offset=start)
    
def numLogs():
    q = db.Query(Log)
    return q.count()
    
def getIPs(start, num):
    q = db.Query(Log, projection=('ip',), distinct=True)
    return q.fetch(limit=num,offset=start)
    
def numIPs():
    q = db.Query(Log, projection=('ip',), distinct=True)
    return q.count()
    
def newLog(ip, message):
    l = Log(ip=ip, # self.request.remote_addr
		message=message)
    l.put()
    
    
class Messages(db.Model):
    message = db.TextProperty(required=True)
    
def getMessage(key):
    # q = db.Query(Messages)
    # q.filter('id=', key)
    # result = q.get()
    # if result is None:
        # return "No message found"
    instance = Messages.get_by_id(int(key))
    if instance is None:
        return "No message found"
    return instance.message
    
def putMessage(message):
    m = Messages(message=message)
    m.put()
    return m.key().id()
    
    
class Page(db.Model):
    name = db.StringProperty(required=True)
    page = db.TextProperty(required=True)

    
def getPage(pagename):
    q = db.Query(Page)
    #import logging
    q.filter('name =', pagename)
    result = q.get()
    if result is None:
        return None
    return result.page
    
def savePage(pagename, data):
    q = db.Query(Page)
    q.filter('name =', pagename)
    result = q.get()
    if result is None:
        p = Page(name=pagename, page=data)
        p.put()
    else:
        result.page = data
        result.put()
    
def numPages():
    q = db.Query(Page)
    return q.count()
    
def getPageNames(start, num):
    q = db.Query(Page, projection=('name',))
    return q.fetch(limit=num,offset=start)

    
class Link(db.Model):
    name = db.StringProperty(required=True)
    link = db.LinkProperty(required=True)
    
def addLink(name, link):
    l = Link(name=name, link=link)
    l.put()
    
def getLinks(start, num):
    q = db.Query(Link)
    q = q.order('-name')
    return q.fetch(limit=num,offset=start)
    

class PublicData(db.Model):
    name = db.StringProperty(required=True)
    
def addPublic(name):
    p = PublicData(name=name)
    p.put()
    
def numPublicData():
    q = db.Query(PublicData)
    return q.count()
    
def getPublic(start, num):
    q = db.Query(PublicData)
    return q.fetch(limit=num,offset=start)
    
def isPublic(name):
    q = db.Query(PublicData)
    q.filter('name =', name)
    result = q.get()
    if result is None:
        return None
    return True
    
def delPublic(name):
    q = db.Query(PublicData)
    q.filter('name =', name)
    result = q.get()
    if result is None:
        return None
    db.delete(result)
    return True
    
    
    