#coding=utf-8

import networkViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$', networkViews.index),
    (r'^networkCls/(?P<orgUid>\w+)/$', networkViews.networkClsIndex),
    (r'^network/(?P<moUid>\w+)/$', networkViews.networkIndex),
    (r'^configGrid/$', networkViews.configGrid),
    (r'^devicesConfigOp/(?P<moUid>\w+)/$', networkViews.devicesConfigOp),
)
