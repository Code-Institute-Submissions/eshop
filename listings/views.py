from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Listing, Category
from .forms import ListingForm, SearchForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q
# Create your views here.


def index(request):
    listings = Listing.objects.all()

    # if there is any search queries submitted
    if request.GET:
        # always true query:
        queries = ~Q(pk__in=[])

        # if a title is specified, add it to the query
        if 'title' in request.GET and request.GET['title']:
            title = request.GET['title']
            queries = queries & Q(title__icontains=title)

        # if a genre is specified, add it to the query
        if 'category' in request.GET and request.GET['category']:
            print("adding category")
            category = request.GET['category']
            queries = queries & Q(category__in=category)

        # update the existing book found
        listings = listings.filter(queries)

    category = Category.objects.all()
    search_form = SearchForm(request.GET)
    return render(request, 'listings/index.template.html', {
        'listings': listings,
        'category': category,
        'search_form': search_form
    }
    )


def view_listing_details(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'listings/details.template.html', {
        'listing': listing
    })


def about(request):
    return render(request, 'about.template.html')


@user_passes_test(lambda u: u.is_superuser)
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"New listing: {form.cleaned_data['title']} created")
            return redirect(reverse(index))
    else:
        # create instance of ListingForm
        form = ListingForm()
        return render(request, 'listings/create_listing.template.html', {
            'form': form
        })


@user_passes_test(lambda u: u.is_superuser)
def edit_listing(request, listing_id):
    listing_being_updated = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing_being_updated)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Listing: {form.cleaned_data['title']} edited")
            return redirect(reverse(index))
    else:
        listing_form = ListingForm(instance=listing_being_updated)
        return render(request, 'listings/edit_listing.template.html', {
            'form': listing_form,
            'listing': listing_being_updated
        })


@user_passes_test(lambda u: u.is_superuser)
def delete_listing(request, listing_id):
    # check if form has been submited via POST
    if request.method == "POST":
        listing_being_deleted = get_object_or_404(Listing, pk=listing_id)
        listing_being_deleted.delete()
        messages.success(
            request, f"{listing_being_deleted.title} has been deleted")
        return redirect(index)
    else:
        # if form not submitted via POST, means its GET
        # display form
        listing_being_deleted = get_object_or_404(Listing, pk=listing_id)
        return render(request, 'listings/confirm_delete.template.html', {
            'listing': listing_being_deleted
        })
