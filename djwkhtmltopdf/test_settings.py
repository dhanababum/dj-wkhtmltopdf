SECRET_KEY = 'woz#_#=zm6rgajn@urjdvv0=wo0p#&_*3ukqpl=$p)v@5-n(+q'

DEBUG = True

TEMPLATE_DEBUG = True

# Installed apps for django >= 1.6
INSTALLED_APPS = ('djwkhtmltopdf',)


# Installed apps for django < 1.6
# and you must install discover_runner for test runs
import django
if django.VERSION < (1, 6):
    INSTALLED_APPS = ('djwkhtmltopdf','discover_runner',)
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

ROOT_URLCONF = 'djwkhtmltopdf.tests.urls'

MIDDLEWARE_CLASSES = tuple()

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

