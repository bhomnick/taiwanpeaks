from django.core.management.base import BaseCommand, CommandError

from photos.models import Photo


class Command(BaseCommand):
    help = 'Update a photo from flickr'

    def add_arguments(self, parser):
        parser.add_argument('photo_id', type=int)

    def handle(self, *args, **options):
        photo_id = options['photo_id']
        try:
            photo = Photo.objects.get(pk=photo_id)
        except Photo.DoesNotExist:
            raise CommandError('Photo "%s" does not exist' % photo_id)

        photo.update_from_flickr()
