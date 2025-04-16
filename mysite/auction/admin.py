from .models import *
from django.contrib import admin


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]


admin.site.register(UserProfile)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Auction)
admin.site.register(Car, CarAdmin)
admin.site.register(Bid)
admin.site.register(Feedback)
