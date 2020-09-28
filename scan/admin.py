from django.contrib import admin
from .models import ScanTable, ScanDetailsTable, Photo


# Register your models here.

class ScanAdmin(admin.ModelAdmin):
    pass


class ScanDetialAdmin(admin.ModelAdmin):
    pass


# class PhotoAdmin(admin.ModelAdmin):
#     pass

admin.site.register(ScanTable, ScanAdmin)
admin.site.register(ScanDetailsTable, ScanDetialAdmin)
# admin.site.register(Photo, PhotoAdmin)
