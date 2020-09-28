from django.contrib import admin
from .models import Order, Billing


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    pass


class BillingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(Billing, BillingAdmin)
