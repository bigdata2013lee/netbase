import eventsViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$',eventsViews.index),
    (r'^history/$', eventsViews.eventHistoryList),
    (r'^config/$', eventsViews.config),
)
