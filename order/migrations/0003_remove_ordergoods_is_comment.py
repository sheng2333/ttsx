# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_ordergoods_is_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordergoods',
            name='is_comment',
        ),
    ]
