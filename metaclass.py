import webapp2
from webapp2_extras import jinja2 as j2

from functools import wraps
import logging


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
    
def inlog(cls):
    orig_get = cls.get
    
    def get(self, q=None):
        import general_counter
        import models
        DEFAULT_COUNTER_NAME = 'TOT'
        
        general_counter.increment(DEFAULT_COUNTER_NAME)
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
    
class logmeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super(logmeta,cls).__new__(cls, clsname, bases, clsdict)
        if len(bases) > 1:
            clsobj = debugmethods(clsobj)
            clsobj = debugcls(clsobj)
            clsobj = inlog(clsobj)
        return clsobj