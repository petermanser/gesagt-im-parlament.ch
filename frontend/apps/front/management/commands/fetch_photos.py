import requests
import os
from PIL import Image, ImageFile
from django.core.management.base import NoArgsCommand
from django.conf import settings
from apps.front import models

#BASE_URL = 'http://www.parlament.ch/SiteCollectionImages/profil/original/'
BASE_URL = 'http://www.parlament.ch/SiteCollectionImages/profil/225x225/'
SIZES = [
    #(225, 225),
    (120, 120),
]

class Command(NoArgsCommand):
    help = 'Fetch and resize photos of the concellors.'

    def printO(self, message):
        """Print to stdout"""
        self.stdout.write(message + '\n')

    def printE(self, message):
        """Print to stderr"""
        self.stderr.write(message + '\n')

    def handle_noargs(self, **options):
        numbers = models.Person.objects.values_list('number', flat=True).filter(number__isnull=False)
        for number in numbers:
            # Fetch file
            url = '%s%s.jpg' % (BASE_URL, number)
            filepath = os.path.join(settings.STATIC_ROOT, 'img', 'portraits')
            response = requests.get(url)

            # Raise exception if bad HTTP status
            try:
                response.raise_for_status()  
            except requests.HTTPError:
                self.printE('Could not fetch %s' % url)
                continue

            # Read file 100KiB at a time
            parser = ImageFile.Parser()
            while 1:
                s = response.read(102400)
                if not s:
                    break
                parser.feed(s)
            
            # Write image at different sizes
            image = parser.close()
            image.save(os.path.join(filepath, '%s-%sx%s.jpg' % (number, 225, 225)))
            for size in SIZES:
                image.thumbnail(size, Image.ANTIALIAS)
                image.save(os.path.join(filepath, '%s-%sx%s.jpg' % (number, size[0], size[1])))
            self.printO('Fetched %s' % url)
