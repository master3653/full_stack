# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_image_total_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='total_likes',
        ),
    ]
