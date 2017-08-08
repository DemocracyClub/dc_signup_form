import binascii
import os
from django.db import models
from django.contrib.postgres.fields import JSONField


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
    data = JSONField()
    mailing_lists = JSONField()
    added = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
