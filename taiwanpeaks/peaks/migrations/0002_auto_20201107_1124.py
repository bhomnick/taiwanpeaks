# Generated by Django 3.1.1 on 2020-11-07 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peaks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='peak',
            options={'ordering': ['rank']},
        ),
    ]
