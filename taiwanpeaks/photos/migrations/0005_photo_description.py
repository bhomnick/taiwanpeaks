# Generated by Django 3.1.1 on 2020-10-05 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_photo_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
