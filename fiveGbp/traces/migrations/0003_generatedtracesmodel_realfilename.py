# Generated by Django 3.1.3 on 2020-12-18 22:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('traces', '0002_auto_20201014_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedtracesmodel',
            name='realFileName',
            field=models.CharField(default=datetime.datetime(2020, 12, 18, 22, 23, 38, 145919, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
