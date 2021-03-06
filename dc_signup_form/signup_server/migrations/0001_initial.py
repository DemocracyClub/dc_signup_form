# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-14 16:49
from __future__ import unicode_literals

import dc_signup_form.signup_server.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignupQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('data', dc_signup_form.signup_server.models.BackwardsCompatibleJSONField()),
                ('mailing_lists', dc_signup_form.signup_server.models.BackwardsCompatibleJSONField()),
                ('added', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('app_name', models.CharField(max_length=100)),
            ],
        ),
    ]
