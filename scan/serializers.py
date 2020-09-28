from rest_framework import serializers
from order.models import Order
from scan.models import ScanTable, ScanDetailsTable


class ScanTableSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    title = serializers.CharField()
    scanImageRaw = serializers.ImageField(allow_null=True, allow_empty_file=True, required=False)
    scanImageUrl = serializers.CharField(allow_blank=True, required=False)

    def save(self, **kwargs):
        try:
            scan = ScanTable.objects.get(order_id=self.validated_data['order_id'])
        except:
            scan = ScanTable()

        order = Order.objects.get(id=self.validated_data['order_id'])
        scan.order = order
        scan.title = self.validated_data['title']
        if 'scanImageUrl' in self.validated_data and self.validated_data['scanImageUrl'] != '':
            scan.scanImageUrl = self.validated_data['scanImageUrl']
            scan.scanImageRaw = None
        else:
            scan.scanImageUrl = None
            scan.scanImageRaw = self.validated_data['scanImageRaw']
        scan.save()
        return scan


class ScanDetailsTableSerializer(serializers.Serializer):
    scan_id = serializers.IntegerField()
    title = serializers.CharField()
    scanDetailImageRaw = serializers.ImageField(allow_null=True, allow_empty_file=True, required=False)
    scanDetailImageUrl = serializers.CharField(allow_blank=True, required=False)

    def save(self, **kwargs):
        scanDetail = ScanDetailsTable()
        scan = ScanTable.objects.get(id=self.validated_data['scan_id'])
        scanDetail.scan = scan
        scanDetail.title = self.validated_data['title']
        if 'scanDetailImageUrl' in self.validated_data and self.validated_data['scanDetailImageUrl'] != '':
            scanDetail.scanDetailImageUrl = self.validated_data['scanDetailImageUrl']
            scanDetail.scanDetailImageRaw = None
        else:
            scanDetail.scanDetailImageUrl = None
            scanDetail.scanDetailImageRaw = self.validated_data['scanDetailImageRaw']
        scanDetail.save()
        return scanDetail
