import monitorViews
from django.conf.urls.defaults import patterns
urlpatterns = patterns('',
    (r'^index/$', monitorViews.index),
    (r'^deviceCls/(?P<orgUid>\w+)/(?P<locUid>\w+)/$', monitorViews.deviceClsIndex),
    (r'^device/(?P<moUid>\w+)/$', monitorViews.deviceIndex),
    (r'^devicesList/$', monitorViews.devicesList),
    (r'^devicesConfigOp/(?P<moUid>\w+)/$', monitorViews.devicesConfigOp),
    (r'^configGrid/$', monitorViews.configGridIndex),
    (r'^configGrid/(?P<orgUid>\w+)/(?P<locUid>\w+)/$', monitorViews.configGrid),
    (r'^device_adds/$', monitorViews.device_adds),
    (r'^upload/$', monitorViews.uploadXlsUsersFile),
    (r'^device_addssusscess/$', monitorViews.device_addssusscess),
)
