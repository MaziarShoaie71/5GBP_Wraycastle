# Generated by Django 3.1 on 2020-11-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiveGApp', '0028_auto_20201101_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='smfmodel',
            name='dnn_dns',
            field=models.CharField(blank=True, default='ipv4:8.8.8.8, ipv6:2001:4860:4860::8888', max_length=200),
        ),
        migrations.AlterField(
            model_name='smfmodel',
            name='dnn',
            field=models.CharField(blank=True, default='internet', max_length=200),
        ),
    ]
