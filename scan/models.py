from django.db import models
from backend import settings
from order.models import Order


# Create your models here.
class ScanTable(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    scanImageRaw = models.ImageField(upload_to='scan/%Y/%m/%d', blank=True, null=True)
    scanImageUrl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "scan_table"

    def get_scan(scan_id):
        try:
            return ScanTable.objects.get(pk=scan_id)
        except ScanTable.DoesNotExist:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order.id,
            'title': self.title,
            'scanImageRaw': settings.BASE_URL + self.scanImageRaw.url if self.scanImageRaw.url else None,
            'scanImageUrl': self.scanImageUrl
        }


class ScanDetailsTable(models.Model):
    scan = models.ForeignKey(ScanTable, on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=255)
    scanDetailImageRaw = models.ImageField(
        blank=True,
        null=True,
        upload_to='scan/%Y/%m/%d'
    )
    scanDetailImageUrl = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "scan_details_table"

    def to_dict(self):
        return {
            'id': self.id,
            'scan_id': self.scan.id,
            'title': self.title,
            'scanDetailImageRaw': settings.BASE_URL + self.scanDetailImageRaw.url if self.scanDetailImageRaw else None,
            'scanDetailImageUrl': self.scanDetailImageUrl
        }

    def array_to_dict(scans):
        details = []
        for ascan in scans:
            temp = {
                'id': ascan.id,
                'scan_id': ascan.scan.id,
                'title': ascan.title,
                'scanDetailImageRaw': settings.BASE_URL + ascan.scanDetailImageRaw.url if ascan.scanDetailImageRaw else None,
                'scanDetailImageUrl': ascan.scanDetailImageUrl
            }
            details.append(temp)
        return details


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='scan/%Y/%m/%d')
    uploaded_at = models.DateTimeField(auto_now_add=True)
