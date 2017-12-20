#coding=utf-8
import os
NBHOME = os.environ["NBHOME"]

loggingConfig = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'filters': {
        'special': {
            #'()': 'project.logging.SpecialFilter',
            #'foo': 'bar',
        }
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '%s/log/mainServer.log' %NBHOME, #/opt/netbase/log/mainServer.log
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'simple',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['default','console'], #for debug
            #'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False,
        },

    }
}