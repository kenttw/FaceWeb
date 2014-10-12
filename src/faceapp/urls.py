# -*- coding: utf-8 -*-
'''
Created on 2014年10月12日

@author: kent
'''
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('faceapp.views',
    url(r'^$', 'list', name='list'),
)