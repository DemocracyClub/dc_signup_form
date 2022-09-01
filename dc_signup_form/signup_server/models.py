import binascii
import os
from django.db import models

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField 


class BackwardsCompatibleJSONField(JSONField):
    # retained for legacy reasons
    # (this used to selectively support json/jsonb, but it doesn't any more)
    def db_type(self, connection):
        return "jsonb"


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
