import assistantViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$',assistantViews.index),
    (r'^shortcutCmd/$',assistantViews.shortcutCmdIndex),
)
