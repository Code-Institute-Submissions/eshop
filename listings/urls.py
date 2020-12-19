from django.contrib import admin
from django.urls import path, include

import listings.views

urlpatterns = [
    path('', listings.views.index),
    path('create/', listings.views.create_listing),
    path('edit/<listing_id>', listings.views.edit_listing,
         name='update_listing_route'),
    path('delete/<listing_id>', listings.views.delete_listing,
         name="delete_listing_route")
]