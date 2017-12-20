import settingsViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$',settingsViews.index),
    (r'^alarm/$', settingsViews.alarm),
    (r'^services/$', settingsViews.services),
    (r'^collector/$', settingsViews.collector),
    (r'^userBilling/$', settingsViews.userBilling),
    (r'^servicesNoteDetail/$', settingsViews.servicesNoteDetail),
    (r'^postComment/$', settingsViews.postComment),
)
