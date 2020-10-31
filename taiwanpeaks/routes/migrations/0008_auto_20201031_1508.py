# Generated by Django 3.1.1 on 2020-10-31 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peaks', '0001_initial'),
        ('routes', '0007_route_custom_permit_info'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='routecabin',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='routecarouselphoto',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='routeitineraryphoto',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='routeitinerarypoint',
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='RoutePeak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('peak', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='routes', to='peaks.peak')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='route_peaks', to='routes.route')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('route', 'peak')},
            },
        ),
    ]