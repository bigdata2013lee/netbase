import reportViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$',reportViews.index),
    (r'^content/(?P<moUid>\w+)/$', reportViews.reportIndex),
    (r'^addreport/$', reportViews.addreport),
)
