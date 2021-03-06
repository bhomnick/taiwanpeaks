# Generated by Django 3.1.1 on 2020-12-05 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_featuredpeak'),
        ('photos', '0005_auto_20201205_0822'),
        ('routes', '0010_route_list_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='routeitinerary',
            options={'ordering': ['day_no'], 'verbose_name': 'itinerary', 'verbose_name_plural': 'itineraries'},
        ),
        migrations.AlterField(
            model_name='cabin',
            name='altitude',
            field=models.IntegerField(help_text='Altitude in meters'),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='booking_link',
            field=models.URLField(blank=True, help_text='Booking URL if cabin is booked separately from permits, for instance Jiaminghu. Leave blank if cabin is booked along with permits.', null=True),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='capacity_beds',
            field=models.IntegerField(blank=True, help_text='Number of bed slots available', null=True),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='capacity_tents',
            field=models.IntegerField(blank=True, help_text='Number of camp sites available', null=True),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='description',
            field=models.TextField(help_text='A description of cabin amenities, water supply, and any special features. Approximately 250-300 characters'),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='latitude',
            field=models.DecimalField(decimal_places=5, help_text='Positive number, 5 decimal places', max_digits=8),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='longitude',
            field=models.DecimalField(decimal_places=5, help_text='Positive number, 5 decimal places', max_digits=8),
        ),
        migrations.AlterField(
            model_name='cabin',
            name='name_zh',
            field=models.CharField(help_text="Cabin's Chinese name, i.e. 南湖山屋", max_length=255, verbose_name='Name (中文)'),
        ),
        migrations.AlterField(
            model_name='route',
            name='active',
            field=models.BooleanField(default=False, help_text='Check to publish for all users. If unchecked only staff users may preview this route.'),
        ),
        migrations.AlterField(
            model_name='route',
            name='cabin_status',
            field=models.CharField(blank=True, choices=[('none', 'No cabins'), ('mixed', 'Mixed cabins/camping'), ('full', 'All cabins')], help_text='All cabins = cabins available every night<br>Mixed cabins/camping = cabins available some nights<br>No cabins = no cabins available, must camp every night', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='custom_permit_info',
            field=models.TextField(blank=True, help_text='Used to override the default permit explanations if special circumstances apply to this route. Leave blank if only regular police/np permits required.', null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='difficulty',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')], help_text='Beginner = tourist-friendly (think Jade)<br>Intermediate = doable with some experience (think Nanhu)<br>Advanced = for experienced hikers (think central sections)<br>Expert = the 4 hurdles (S3, Mabo, Qilai East, Ganzhuowan)<br>If unsure ask for opinions.', max_length=50),
        ),
        migrations.AlterField(
            model_name='route',
            name='header_background_photo',
            field=models.ForeignKey(help_text='Photo will appear behind route name/header.', on_delete=django.db.models.deletion.PROTECT, related_name='header_background_routes', to='photos.photo'),
        ),
        migrations.AlterField(
            model_name='route',
            name='intro',
            field=models.TextField(help_text='Short intro describing the highlights of this route. Approximately 400-500 characters.'),
        ),
        migrations.AlterField(
            model_name='route',
            name='list_description',
            field=models.TextField(blank=True, help_text='Short route description used in the routes list view. No more than 120 characters.', null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='locations',
            field=models.ManyToManyField(help_text='Select any locations this route crosses. Many routes cross more than one.', to='common.Location'),
        ),
        migrations.AlterField(
            model_name='route',
            name='name_zh',
            field=models.CharField(help_text='Route name in Chinese, i.e. 北一段', max_length=255, verbose_name='Name (中文)'),
        ),
        migrations.AlterField(
            model_name='route',
            name='np_permit_required',
            field=models.CharField(blank=True, choices=[('taroko', 'Taroko National Park'), ('sheipa', 'Shei-pa National Park'), ('jade', 'Yushan National Park')], help_text='Select the appropriate park if a national park entry permit is required.', max_length=50, null=True, verbose_name='National Park Permit Required'),
        ),
        migrations.AlterField(
            model_name='route',
            name='peak_count',
            field=models.IntegerField(help_text='Total number of top 100 peaks covered by this route.'),
        ),
        migrations.AlterField(
            model_name='route',
            name='police_permit_required',
            field=models.BooleanField(help_text='Check if police mountain entry permit required.'),
        ),
        migrations.AlterField(
            model_name='route',
            name='public_transport_accessible',
            field=models.BooleanField(help_text='Check is trailheads are accessible via public transport.'),
        ),
        migrations.AlterField(
            model_name='route',
            name='summary_background_photo',
            field=models.ForeignKey(help_text='Photo will appear behind route summary section.', on_delete=django.db.models.deletion.PROTECT, related_name='summary_background_routes', to='photos.photo'),
        ),
        migrations.AlterField(
            model_name='route',
            name='total_distance',
            field=models.IntegerField(help_text='Total route distance in km.'),
        ),
        migrations.AlterField(
            model_name='route',
            name='transportation_desc',
            field=models.TextField(blank=True, help_text='Describe how to get to the trailhead, any public transportation options, the parking situation, etc.', null=True, verbose_name='Transportation description'),
        ),
        migrations.AlterField(
            model_name='route',
            name='transportation_link',
            field=models.URLField(blank=True, help_text='An optional link to bus schedule or other external transportation resource.', null=True),
        ),
        migrations.AlterField(
            model_name='routeitinerary',
            name='day_no',
            field=models.IntegerField(verbose_name='day number'),
        ),
        migrations.AlterField(
            model_name='routeitinerary',
            name='rest_name',
            field=models.CharField(blank=True, help_text='Name of cabin or campsite', max_length=255, null=True, verbose_name='Shelter name'),
        ),
        migrations.AlterField(
            model_name='routeitinerary',
            name='rest_type',
            field=models.CharField(blank=True, choices=[('cabin', 'Cabin'), ('campground', 'Campground')], max_length=50, null=True, verbose_name='Shelter type'),
        ),
        migrations.AlterField(
            model_name='routeitinerary',
            name='total_distance',
            field=models.DecimalField(decimal_places=1, help_text='Total distance for the day in kilometers', max_digits=3),
        ),
        migrations.AlterField(
            model_name='routeitinerary',
            name='total_hours',
            field=models.DecimalField(decimal_places=1, help_text='Total hiking time for the day in hours', max_digits=3),
        ),
        migrations.AlterField(
            model_name='routeitinerary',
            name='water_desc',
            field=models.CharField(blank=True, help_text='Brief description of water source. Include location and reliability.', max_length=255, null=True, verbose_name='Water description'),
        ),
    ]
