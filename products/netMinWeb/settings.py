# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from products.netMinWeb.loggingconfig import loggingConfig
from products.netUtils.settings import MemCacheSettings



DEBUG = True
TEMPLATE_DEBUG = DEBUG

APP_PATH = os.path.split(__file__)[0]
ROOT_PATH = os.path.split(APP_PATH)[0]

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

SVN = ''
MANAGERS = ADMINS


#email config
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'notice@safedragon.com.cn'
EMAIL_HOST_PASSWORD = "netbase123"


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = APP_PATH + os.sep + "media"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media'
#静态文件防止发布的时候，浏览器还缓存可以设置 MEDIA_URL = "/svnNum/media/" 这样每次更新的时候，url改变，浏览器就不会缓存了。但是页面中要使用变量

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

LOGIN_REDIRECT_URL = 'index/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^0ia9wkc=1=f_kyhsgd0#50d4c*vqfybmlobma+q_g!c(x0-qw_abc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.media",   
    "django.core.context_processors.request",
)   

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'products.netMinWeb.netMiddleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'netMinWeb.urls'

TEMPLATE_DIRS = (
    APP_PATH + os.sep + 'templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

AUTHENTICATION_BACKENDS = (
    'netMinWeb.authBackend.NetBaseBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'products.netMinWeb',
)

#memcache作为后台Session缓存引擎
mcs=MemCacheSettings.getSettings()
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%s:%s' %(mcs.get("session","host"),mcs.get("session","port")),
        'TIMEOUT': 24*60*60  #24小时有效
    }
}

SESSION_COOKIE_NAME="session_id"
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
#设置浏览器关闭时默认就是False，session也有效，SESSION_COOKIE_AGE设置的时间
SESSION_EXPIRE_AT_BROWSER_CLOSE = False 
SESSION_COOKIE_AGE = 86400 #24小时有效
SESSION_SAVE_EVERY_REQUEST = True

LOGGING = loggingConfig


if __name__  == "__main__":
    print __file__
