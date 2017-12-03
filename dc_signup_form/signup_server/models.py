import binascii
import os
from django.db import models

try:
    # django < 2.0
    from django.db.backends.postgresql_psycopg2.version import get_version
except ImportError:
    # django >= 2.0
    from django.db import connection
    def get_version(connection):
        return connection.pg_version

from django.contrib.postgres.fields import JSONField


class BackwardsCompatibleJSONField(JSONField):
    def db_type(self, connection):
        if get_version(connection) < 90400:
            return 'json'
        return 'jsonb'


class Token(models.Model):
    token = models.CharField(max_length=40, primary_key=True)
    app_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.token = self.generate_token()
        return super(Token, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.app_name


class SignupQueue(models.Model):
    email = models.EmailField()
    data = BackwardsCompatibleJSONField()
    mailing_lists = BackwardsCompatibleJSONField()
    added = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
