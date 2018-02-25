#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
root = lambda *x: os.path.join(BASE_DIR, *x)

if not settings.configured:
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
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.staticfiles',

            'dc_theme',

            'test_project',

            'dc_signup_form',
            'dc_signup_form.signup_server',
        ),
        ROOT_URLCONF='test_project.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'DIRS': [
                    root('test_project/templates'),
                ],
                'OPTIONS': {
                    'debug': True,
                    'context_processors': [
                        'dc_theme.context_processors.dc_theme_context',
                        'dc_signup_form.context_processors.signup_form',
                    ],
                },
            }
        ],
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
    )

django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
failures = test_runner.run_tests(['dc_signup_form', ])
sys.exit(failures)
