# -*- coding:utf-8 -*-
__author__ = 'Lin_Tong'
from django.http import HttpResponseBadRequest

def ajax_required(f):
    def wrap(request,*args,**kwargs):
        if not request.is_ajax():   #不是ajax请求时返回404
            return HttpResponseBadRequest()
        return f(request,*args,**kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap