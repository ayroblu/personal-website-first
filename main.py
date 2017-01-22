import webapp2
#import re
#import base64
# import json
from webapp2_extras import jinja2 as j2
# from google.appengine.api import users
import general_counter
DEFAULT_COUNTER_NAME = 'TOT'

import models

from metaclass import debugmeta, logmeta


class Main:
    __metaclass__ = debugmeta
    @webapp2.cached_property
    def jinja2(self):
        return j2.get_jinja2(app=self.app)
        
    def render_response(self, template, **context):
        rendered_value = self.jinja2.render_template(template, **context)
        self.response.write(rendered_value)
        
class MetaMain:
    __metaclass__ = logmeta
    @webapp2.cached_property
    def jinja2(self):
        return j2.get_jinja2(app=self.app)
        
    def render_response(self, template, **context):
        rendered_value = self.jinja2.render_template(template, **context)
        self.response.write(rendered_value)

class MainHandler(MetaMain, webapp2.RequestHandler):        
    def get (self, q=None):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        if q is None:
            q = "index.html"
        self.render_response(q, general_total=general_total)


class home(MetaMain, webapp2.RequestHandler):        
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("home.html", general_total=general_total)
        
        
class vi(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("vi.html", general_total=general_total)


class vi2(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("vi2.html", general_total=general_total)


class emacs(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("emacs.html", general_total=general_total)


class lyrics(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        message = ''#dir(self.request)
        self.render_response("lyrics.html", general_total=general_total, message=message)


class getLyric(Main, webapp2.RequestHandler):
    def get(self):
        song = self.request.get('s')
        if song:
            import os
            files = [f for f in os.listdir('templates/lyrics') if f.lower().find(song.lower()) >= 0]
            if not files: #No file found
                gsearch = "<a href=\"http://www.google.com/search?q=%s lyrics\">Google search</a>" % song.replace('"','&quot')
                self.response.out.write("No lyric found try %s" % gsearch)
            elif len(files) == 1: #Found a file - pulling and showing
                self.response.out.write(files[0]+"----\n\n")
                self.render_response('lyrics/'+files[0])
            else: #list of available files
                self.response.out.write("\n".join(files))
        else: # Shouldn't be called, null output
            self.response.out.write("")


class ip(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        ip = self.request.remote_addr
        self.render_response("ip.html", general_total=general_total, ip=ip)


class car(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("car.html", general_total=general_total)

        
class hug(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("hug.html", general_total=general_total)

class details(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("details.html", general_total=general_total)

        
class hack(MetaMain, webapp2.RequestHandler):
    def get (self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("hack.html", general_total=general_total)
        

class message(MetaMain, webapp2.RequestHandler):
    def get (self, m=None):
        if m is None:
            general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
            self.render_response("message_creator.html", general_total=general_total)
        else:
            # Display some message page
            # Message from database
            # key = base64.b64decode(m)
            import functions
            key = functions.base62_decode(str(m))
            messages = models.getMessage(key)
            messages = [str(i) for i in messages.split('\r\n')]
            self.render_response("messages.html", messages=messages)
        
        #message = ['So, just a quick test','I can define any message now','Verified']
        #self.render_response("messages.html", messages=message)
    
    def post(self, m=None):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
            
        message = self.request.get("message")
        id = models.putMessage(message)
        # b64id = base64.b64encode(str(id))
        b64id = functions.base62_encode(id)
        page = 'ben-lu.appspot.com/m'+b64id
        # return self.response.out.write("<h1>Message created</h1>\
            # <a href='/m"+b64id+"'>id = "+str(id)+", b64id = "+b64id+"</a>")
        self.render_response("message_created.html", general_total=general_total, page=page)
    

"""class login(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/home')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/admin'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)"""
        
class logger(Main, webapp2.RequestHandler):
    def get(self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        
        count = models.numLogs()
        import logging
        logging.info('Number of logs: %i' % count)
        
        start = self.request.get("s")
        if type(start) != int and start:
            try:
                start = int(start)
            except Exception as e:
                logging.info('Error found: %s' % e)
        if not start:
            start = 0
            logging.info('if not start has run')
        elif start < 0 or start >= count:
            logging.info('%s < 0 or %s >= %s' % (start,start,count))
            start = 0
        
        if start - 100 >= 0:
            previous = start - 100
        else:
            previous = -1
        if start + 100 < count:
            next = start + 100
        else:
            next = -1
        
        result = models.getLogs(start, 100)
        logging.info('result = models.getLogs(%s, 100)' % str(start))
        vals = {
            'general_total':general_total,
            'logs':result,
            'next':next,
            'previous':previous
        }
        self.render_response("logger.html", **vals)
    
class iplogger(Main, webapp2.RequestHandler):
    def get(self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        
        count = models.numIPs()
        logging.info('Number of logs: %i' % count)
        
        start = self.request.get("s")
        if type(start) != int and start:
            try:
                start = int(start)
            except Exception as e:
                logging.info('Error found: %s' % e)
        if not start:
            start = 0
            logging.info('if not start has run')
        elif start < 0 or start >= count:
            logging.info('%s < 0 or %s >= %s' % (start,start,count))
            start = 0
        
        if start - 100 >= 0:
            previous = start - 100
        else:
            previous = -1
        if start + 100 < count:
            next = start + 100
        else:
            next = -1
        
        result = models.getIPs(start, 100)
        logging.info('result = models.getLogs(%s, 100)' % str(start))
        vals = {
            'general_total':general_total,
            'logs':result,
            'next':next,
            'previous':previous
        }
        self.render_response("logger.html", **vals)
    
class about(MetaMain, webapp2.RequestHandler):
    def get(self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("about.html", general_total=general_total)
        
class regex(MetaMain, webapp2.RequestHandler):
    def get(self):
        general_total = general_counter.get_count(DEFAULT_COUNTER_NAME)
        self.render_response("regex.html", general_total=general_total)
        
class out(MetaMain, webapp2.RequestHandler):
    def get(self):
        page = self.request.get('p')
        if page:
            pagedata = models.getPage(page)
            if pagedata:
                context = {}
                self.response.write(j2.jinja2.Template(pagedata).render(context))
            else:
                self.response.write("<h1>No.</h1>")
        else:
            self.response.write("<h1>Who are you...?</h1>")
            
            



app = webapp2.WSGIApplication([
    ('/home',home),
    ('/hug',hug),
    ('/details',details),
    ('/hack',hack),
    ('/vi',vi),
    ('/vi2',vi2),
    ('/emacs',emacs),
    ('/lyrics',lyrics),
    ('/l',getLyric),
    ('/ip',ip),
    ('/car',car),
    ('/regex',regex),
    # ('/login',login),
    ('/logger',logger),
    ('/iplogger',iplogger),
    ('/about',about),
    ('/out',out),
    ('/m(.+)?',message),
    ('/(.*html)?', MainHandler)
])
