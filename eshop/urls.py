"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import listings.views
import reviews.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('listings/', listings.views.index),
    path('reviews/', reviews.views.index),
    path('sellers/', listings.views.view_sellers),
    path('create_listing/', listings.views.create_listing),
    path('edit_listing/<listing_id>', listings.views.edit_listing,
         name='update_listing_route'),
    path('delete_listing/<listing_id>', listings.views.delete_listing,
         name="delete_listing_route")
]
