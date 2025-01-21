from django.core.management.base import BaseCommand
from django.conf import settings
from geographical.models import Barangay
from geographical.utils import geocode_address


class Command(BaseCommand):
    help = "Insert or sync the geolocation (latitude and longitude) for barangays defined in settings.py"

    def handle(self, *args, **options):
        barangay_names = settings.BARANGAYS

        if not barangay_names:
            self.stdout.write(self.style.ERROR("No barangays defined in settings.py!"))
            return

        for barangay_name in barangay_names:
            lat, lng = geocode_address(barangay_name)

            if lat is not None and lng is not None:
                barangay, created = Barangay.objects.get_or_create(
                    name=barangay_name,
                    defaults={'latitude': lat, 'longitude': lng}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully inserted {barangay_name} with geolocation'))
                else:
                    self.stdout.write(self.style.WARNING(f'Barangay "{barangay_name}" already exists'))

            else:
                self.stdout.write(self.style.WARNING(f'Failed to get geolocation for {barangay_name}'))

        self.stdout.write(self.style.SUCCESS('Geolocation sync for specified barangays completed!'))
