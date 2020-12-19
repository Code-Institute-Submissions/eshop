from django.contrib import admin

from .models import Listing, Brand, Seller, Category

# Register your models here.
admin.site.register(Listing)
admin.site.register(Brand)
admin.site.register(Seller)
admin.site.register(Category)
# admin.site.register(Condition)