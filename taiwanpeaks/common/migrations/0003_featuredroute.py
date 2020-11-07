# Generated by Django 3.1.1 on 2020-11-07 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0010_route_list_description'),
        ('common', '0002_location_name_short'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='routes.route')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]