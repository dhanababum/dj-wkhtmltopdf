#! /usr/bin/env python
import sys
import os
import django

from django.conf import settings


APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        'djwkhtmltopdf',
        'djwkhtmltopdf.tests',
    ),
    ROOT_URLCONF = "djwkhtmltopdf.tests.urls",
)

if django.VERSION >= (1, 7):
    django.setup()

try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from discover_runner.runner import DiscoverRunner


test_runner = DiscoverRunner(verbosity=1)
failures = test_runner.run_tests(['djwkhtmltopdf'])
if failures:
    sys.exit(1)
