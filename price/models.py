from django.db import models


# Create your models here.
class Price(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    old_price = models.FloatField()
    unit = models.CharField(max_length=255)

    class Meta:
        db_table = 'price'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'old_price': self.old_price,
            'unit': self.unit,
        }
