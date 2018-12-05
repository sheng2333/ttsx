# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordergoods',
            name='is_comment',
            field=models.BooleanField(verbose_name='是否评价', default=False),
        ),
    ]
