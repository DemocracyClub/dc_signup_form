# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("signup_server", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE signup_server_signupqueue
            ALTER COLUMN data
            SET DATA TYPE jsonb
            USING data::jsonb;""",
            reverse_sql="""
            ALTER TABLE signup_server_signupqueue
            ALTER COLUMN data
            SET DATA TYPE json
            USING data::json;""",
        ),
        migrations.RunSQL(
            """
            ALTER TABLE signup_server_signupqueue
            ALTER COLUMN mailing_lists
            SET DATA TYPE jsonb
            USING mailing_lists::jsonb;""",
            reverse_sql="""
            ALTER TABLE signup_server_signupqueue
            ALTER COLUMN mailing_lists
            SET DATA TYPE json
            USING mailing_lists::json;""",
        ),
    ]
