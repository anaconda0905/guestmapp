from django.db import models
from users.models import User


class Order(models.Model):
    """
    Order Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    choices = (
        (0, 'Blueprint'),
        (1, 'Themed 3D staging'),
        (2, 'Custom interio design 3D'),
        (3, 'Custom mobile home 3D'),
    )
    product_type = models.IntegerField(default=0, choices=choices)
    # selected_theme = models.IntegerField()
    metadata = models.CharField(max_length=1024, null=True)
    tires = models.IntegerField()
    currency = models.CharField(max_length=10)
    price = models.FloatField(blank=True, null=True)

    statusChoices = (
        (0, 'pending'),
        (1, 'ready'),
        (2, 'working'),
        (3, 'completed'),
        (4, 'cancelled'),
        (5, 'confirmed'),
    )
    status = models.IntegerField(default=0, choices=statusChoices)
    created_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "order"

    def __str__(self):
        return "order" + str(self.id)

    def get_order(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return None

    def to_dict(self):
        return {
            'id': self.id,
            'productType': self.product_type,
            # 'selectedTheme': self.selected_theme,
            'metadata': self.metadata,
            'tires': self.tires,
            'price': self.price,
            'status': self.status,
            'createdTime': self.created_date,
            'completedTime': self.completed_date,
        }

    def getImageUrl(self):
        from scan.models import ScanTable
        scan, created = ScanTable.objects.get_or_create(order=self)
        return scan.scanImageUrl

    def getProjectTitle(self):
        from scan.models import ScanTable
        scan, created = ScanTable.objects.get_or_create(order=self)
        return scan.title

    def productTitle(self):
        productType = {
            0: 'Blueprint',
            1: 'Themed 3D staging',
            2: 'Custom interio design 3D',
            3: 'Custom mobile home 3D'
        }
        return productType.get(self.product_type)

    def productImage(self):
        product_image = {
            0: 'blueprint',
            1: 'eyeview',
            2: 'custom3d',
            3: 'custom3d'
        }
        return product_image.get(self.product_type)

    def orderStatus(self):
        status = {
            0: 'Pending',
            1: 'Ready',
            2: 'working',
            3: 'completed',
            4: 'cancelled',
            5: 'confirmed'
        }
        return status.get(self.status)

    def get_price(self):
        return round(self.price/100, 2)

class Billing(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    cvv = models.IntegerField()
    price = models.FloatField(blank=True, null=True)
    expiry_date = models.CharField(max_length=255)
    transaction_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'billing'

    def __str__(self):
        return "billing" + str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'card_name': self.card_name,
            'card_number': self.card_number,
            'cvv': self.cvv,
            'price': self.price,
            'expiry_date': self.expiry_date,
            'transaction_code': self.transaction_code,
        }
