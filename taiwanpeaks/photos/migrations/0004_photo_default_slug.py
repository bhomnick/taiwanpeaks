# Generated by Django 3.1.1 on 2020-11-05 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_photo_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='default_slug',
            field=models.BooleanField(default=False),
        ),
    ]
