from django.shortcuts import render
from .models import Listing, Seller

# Create your views here.


def index(request):
    all_listings = Listing.objects.all()
    return render(request, 'listings/index.template.html', {
        'listings': all_listings
    }
    )


def view_sellers(request):
    all_sellers = Seller.objects.all()
    return render(request, 'listings/sellers.template.html', {
        'sellers': all_sellers
    })