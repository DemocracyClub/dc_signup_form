import django
from django.conf import settings
from django.core.management import call_command


if not settings.configured:
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=(
            "django.contrib.contenttypes",
            "dc_signup_form",
            "dc_signup_form.signup_server",
        ),
    )

django.setup()
call_command("makemigrations", "dc_signup_form")
call_command("makemigrations", "signup_server")
