from django.contrib import admin
from hometype.models import HomeType


# Register your models here.
class HomeTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(HomeType, HomeTypeAdmin)
