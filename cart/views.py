from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.contrib import messages
from listings.models import Listing

# Create your views here.


def add_to_cart(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # initialize the shopping cart if it does not exist
    # or fetch the cart if it does
    cart = request.session.get('shopping_cart', {})

    # the listing is not in the shopping cart
    if listing_id not in cart:
        cart[listing_id] = {
            'id': listing_id,
            'title': listing.title,
            'cost': "{:.2f}".format(listing.cost/100),
            'qty': 1
        }
    else:
        # if the shopping cart already has the listing,
        # then we assume the user want to buy an additional copy
        cart[listing_id]['qty'] += 1

    request.session['shopping_cart'] = cart
    messages.success(request, "listing has been added to your shopping cart")
    return redirect(reverse('view_listing_route'))


def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    return render(request, 'cart/view_cart.template.html', {
        'cart': cart
    })


def remove_from_cart(request, listing_id):
    cart = request.session.get('shopping_cart', {})

    # check if a key in the cart dictionary that matches the listing_id
    if listing_id in cart:
        del cart[listing_id]

        # re-save the session
        request.session['shopping_cart'] = cart
        messages.success(request, "Item succesfully removed from cart")

    return redirect(reverse('view_listing_route'))


def update_quantity(request, listing_id):
    cart = request.session.get('shopping_cart', {})
    # if the listing_id I want to update the quantity is in the shopping cart
    if listing_id in cart:
        cart[listing_id]['qty'] = request.POST['qty']
        request.session['shopping_cart'] = cart
        messages.success(request, "Quantity has been updated")

    return redirect(reverse('view_cart'))