# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PHOTO',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(max_length=10000, null=True, upload_to=b'photos/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
