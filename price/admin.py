from django.contrib import admin
from price.models import Price


# Register your models here.
class PriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Price, PriceAdmin)
