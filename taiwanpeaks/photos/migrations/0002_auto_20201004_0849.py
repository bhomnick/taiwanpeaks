# Generated by Django 3.1.1 on 2020-10-04 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='attr_author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='attr_license',
            field=models.CharField(blank=True, choices=[('cc0', 'CC0 1.0'), ('pdm', 'PDM'), ('cc_by', 'CC BY 2.0'), ('cc_by_sa', 'CC BY-SA 2.0'), ('cc_by_nc', 'CC BY-NC 2.0'), ('cc_by_nd', 'CC BY-ND 2.0'), ('cc_by_nc_sa', 'CC BY-NC-SA 2.0'), ('cc_by_nc_nd', 'CC BY-NC-ND 2.0')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='attr_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='attr_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]