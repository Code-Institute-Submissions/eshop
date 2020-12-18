from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from .models import Listing, Seller
from .forms import ListingForm
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


def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(index))
    else:
        # create instance of ListingForm
        create_listing_form = ListingForm()
        return render(request, 'listings/create_listing.template.html', {
            'form': create_listing_form
        })


def edit_listing(request, listing_id):
    listing_being_updated = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing_being_updated)
        if form.is_valid():
            form.save()
            return redirect(reverse(index))
    else:
        listing_form = ListingForm(instance=listing_being_updated)
        return render(request, 'listings/edit_listing.template.html', {
            'form': listing_form,
            'listing': listing_being_updated
        })


def delete_listing(request, listing_id):
    listing_being_deleted = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'listings/confirm_delete.template.html', {
        'listing': listing_being_deleted
    })
