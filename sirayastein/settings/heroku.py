import dj_database_url

from .base import *

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

DATABASES = {'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

LOGGING = {
    'version': 1,
    # The version number of our log
    'disable_existing_loggers': False,
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    'loggers': {
       # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        '': {
            'handlers': ['console'], #notice how file variable is called in handler which has been defined above
            'level': 'WARNING',
            'propagate': True,
            'formatter': 'verbose',
        },
    },

}