# Generated by Django 3.1.3 on 2020-11-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiveGApp', '0038_udrmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='nssfModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='upfModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('upfName', models.CharField(blank=True, default='UPF', max_length=50)),
                ('debugLevel', models.CharField(blank=True, default='info', max_length=50)),
                ('pfcp', models.CharField(blank=True, default='[{addr: 10.200.200.101}]', max_length=600)),
                ('gtpu', models.CharField(blank=True, default='[{addr: 10.200.200.102}]', max_length=600)),
                ('dnn_list', models.CharField(blank=True, default='[{dnn:internet, cidr:60.60.0.0/24}]', max_length=600)),
            ],
            options={
                'verbose_name': 'UPF Config',
                'verbose_name_plural': 'UPF Config',
            },
        ),
        migrations.AlterField(
            model_name='ausfmodel',
            name='plmnSupportList',
            field=models.CharField(blank=True, default='[{mcc: 208, mnc: 93}, {mcc: 123, mnc: 45}]', max_length=100),
        ),
    ]
