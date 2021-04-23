CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'dj_assessment_default_cache',
        'TIMEOUT': 3600
    }
}
CACHES['sessions'] = CACHES['default']
CACHES['local'] = CACHES['default']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_assessment.db',
    }
}
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_assessment',
]


SECRET_KEY = 'sxjatWnuNyHxh4UCkF9UnXB2JIQOEiWQ84xqVMkBnCc'
