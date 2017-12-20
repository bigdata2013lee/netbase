import messageViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$',messageViews.index),
    (r'^content/(?P<moUid>\w+)/$', messageViews.reportIndex),
    (r'^addreport/$', messageViews.addreport),
)
