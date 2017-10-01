#!/usr/bin/env python
import os
import sys
import django
from distutils.version import StrictVersion
from django.conf import settings
from django.test.utils import get_runner


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = lambda *x: os.path.join(BASE_DIR, *x)

if not settings.configured:

    INSTALLED_APPS = (
        'django.contrib.contenttypes',
        'dc_signup_form',
    )
    if StrictVersion(django.get_version()) >= '1.9.0':
        INSTALLED_APPS += ('dc_signup_form.signup_server',)

    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'test',
                'USER': 'postgres',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        },
        INSTALLED_APPS=INSTALLED_APPS,
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'DIRS': [
                    root('templates'),
                ],
                'OPTIONS': {
                    'debug': True,
                    'context_processors': [],
                },
            }
        ]
    )

django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
failures = test_runner.run_tests(['dc_signup_form', ])
sys.exit(failures)
