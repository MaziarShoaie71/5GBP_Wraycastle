# Generated by Django 3.1 on 2020-11-01 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiveGApp', '0027_smfmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='smfmodel',
            options={'verbose_name': 'SMF Config', 'verbose_name_plural': 'SMF Config'},
        ),
        migrations.AlterField(
            model_name='smfmodel',
            name='pfcp_addr',
            field=models.CharField(blank=True, default='127.0.0.1 ', max_length=50),
        ),
        migrations.AlterField(
            model_name='smfmodel',
            name='sbi_port',
            field=models.IntegerField(blank=True, default=29502),
        ),
    ]
