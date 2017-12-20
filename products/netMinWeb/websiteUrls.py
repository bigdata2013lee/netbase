import websiteViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$',websiteViews.index),
    (r'^add/$',websiteViews.website_add),
    (r'^conf/(?P<websiteUid>\w+)/$',websiteViews.website_conf),
    (r'^detail/(?P<websiteUid>\w+)/$',websiteViews.website_detail),
    (r'^websiteCls/(?P<orgUid>\w+)/$', websiteViews.websiteClsIndex),
    (r'^config/$',websiteViews.config),
)
