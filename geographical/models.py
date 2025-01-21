from django.db import models


class Barangay(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }
