import os
import webapp2
import functions
from webapp2_extras import jinja2 as j2
from google.appengine.api import users

import models
import general_counter

DEFAULT_COUNTER_NAME = 'TOT'

from functools import wraps
import logging

logging.info('**************admin.py**************')

def debug(func):
    msg = '-------------------'+func.__name__+'----------------------'
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(msg)
        return func(*args, **kwargs)
    return wrapper

def debugmethods(cls):
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))
    return cls
    
def debugcls(cls):
    orig_get = cls.get
    
    def get(self, q=None):
        msg = '===============Get Class: '+cls.__name__+'==============='
        logging.info(msg)
        if q is None:
            return orig_get(self)
        else:
            return orig_get(self, q)
    cls.get = get
    
    return cls
    
def logger(cls):
    orig_get = cls.get
    
    def get(self, q=None):
        models.newLog(self.request.remote_addr, 'request '+cls.__name__)
        if q is None:
            return orig_get(self)
        else:
            return orig_get(self, q)
    cls.get = get
    
    return cls

    
class debugmeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super(debugmeta,cls).__new__(cls, clsname, bases, clsdict)
        if len(bases) > 1:
            clsobj = debugmethods(clsobj)
            clsobj = debugcls(clsobj)
        return clsobj
    

class Main:
    __metaclass__ = debugmeta
    @webapp2.cached_property
    def jinja2(self):
        return j2.get_jinja2(app=self.app)
        
    def render_response(self, template, **context):
        rendered_value = self.jinja2.render_template(template, **context)
        self.response.write(rendered_value)

class admin(Main, webapp2.RequestHandler):        
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        page = self.request.get('p')
        editor = self.request.get('e')
        logging.info("page: %s, editor: %s" % (str(page), str(editor)))
        if page: # for example if page == test
            pagedata = models.getPage(page)
            if pagedata:
                context = {}
                self.response.write(j2.jinja2.Template(pagedata).render(context))
            else:
                self.response.write("<h1>No.</h1>")
        elif editor:
            pagedata = models.getPage(editor)
            if pagedata:
                self.render_response("editor.html", general_total=general_total, pagedata=pagedata, name=editor)
            else:
                self.render_response("editor.html", general_total=general_total, pagedata='', name=editor)
        else:
            vals = self.getData()
            self.render_response("admin.html", **vals)
                
        # self.response.write(j2.jinja2.Template('<h1>Hello {{ name }}!</h1>').render(name="John Doe"))
        
    def post(self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        page = self.request.get("message")
        name = self.request.get("name")
        models.savePage(name,page)
        #self.render_response("admin.html", general_total=general_total)
	self.response.write("Y")
        
    def getData(self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        
        count = models.numPages()
        start = self.request.get("s")
        num = 20
        
        if type(start) != int and start:
            try:
                start = int(start)
            except Exception as e:
                start = 0
                logging.info('Error found: %s' % e)
                
        if not start:
            start = 0
        elif start < 0 or start >= count:
            start = 0
        
        if start - num >= 0:
            previous = start - num
        else:
            previous = -1
            
        if start + num < count:
            next = start + num
        else:
            next = -1
        
        result = models.getPageNames(start, num)
        #logging.info('result = models.getLogs(%s, 100)' % str(start))
        return {
            'general_total':general_total,
            'pages':result,
            'next':next,
            'previous':previous
        }
        
        
class login(Main, webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)
    
    
class publicData(Main, webapp2.RequestHandler):
    def get(self):
        vals = self.getData(20)
        self.render_response("publicdata.html", **vals)
        
    def getData(self, num):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        
        count = models.numPages()
        start = self.request.get("s")
        
        if type(start) != int and start:
            try:
                start = int(start)
            except Exception as e:
                start = 0
                logging.info('Error found: %s' % e)
                
        if not start or start < 0 or start >= count:
            start = 0
        
        if start - num >= 0:
            previous = start - num
        else:
            previous = -1
            
        if start + num < count:
            next = start + num
        else:
            next = -1
        
        result = models.getPageNames(start, num)
        #logging.info('result = models.getLogs(%s, 100)' % str(start))
        return {
            'general_total':general_total,
            'pages':result,
            'next':next,
            'previous':previous
        }

    
class addPublic(Main, webapp2.RequestHandler):
    def get(self):
        self.redirect("/admin/publicData")

    def post(self):
        name = self.request.get("name")
        models.addPublic(name)
        #redirect...
        self.redirect("/admin/publicData")

        
class deletePublic(Main, webapp2.RequestHandler):
    def get(self):
        self.redirect("/admin/publicData")

    def post(self):
        name = self.request.get("name")
        models.delPublic(name)
        #redirect...
        self.redirect("/admin/publicData")
        

app = webapp2.WSGIApplication([
    ('/admin',admin),
    #('/admin/publicdata',publicData),
    # ('/admin',login),
])
