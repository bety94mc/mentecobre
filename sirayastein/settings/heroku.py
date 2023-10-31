import dj_database_url

from .base import *

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

DATABASES = {'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
