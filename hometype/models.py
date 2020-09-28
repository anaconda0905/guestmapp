from django.db import models
from backend import settings


# Create your models here.
class HomeType(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='hometype', blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    manufacture = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "hometype"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': settings.BASE_URL + self.image.url if self.image.url else None,
            'model': self.model,
            'manufacture': self.manufacture,
        }
