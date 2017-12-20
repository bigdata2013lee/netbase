#coding=utf-8

import templateViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^thresholdList/(?P<uid>\w+)/(?P<cType>\w+)/$', templateViews.thresholdList),
)
