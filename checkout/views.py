from django.shortcuts import render, get_object_or_404, reverse, HttpResponse
from listings.models import Listing
from .models import Purchase

import stripe
import json
from django.conf import settings
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Create your views here.


def checkout(request):
    # set the api keys for stripe to work
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # retrieve the shopping cart
    cart = request.session.get('shopping_cart', {})

    line_items = []
    all_listing_ids = []

    # go through each item in the shopping cart
    for listing_id, cart_item in cart.items():

        # retrieve the listing specified by listing_id
        listing_model = get_object_or_404(Listing, pk=listing_id)

        # create the line item
        # for the line item, each key in the dictionary is prefixed  by Stripes
        item = {
            "name": listing_model.title,
            "amount": listing_model.price,
            "quantity": cart_item['qty'],
            "currency": 'usd'
        }

        line_items.append(item)
        all_listing_ids.append({
            'listing_id': listing_model.id,
            'qty': cart_item['qty']
        })

    current_site = Site.objects.get_current()
    domain = current_site.domain

    # create a payment session (it's for Stripe)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        client_reference_id=request.user.id,
        metadata={
            'all_listing_ids': json.dumps(all_listing_ids)
        },
        mode="payment",
        success_url=domain + reverse('checkout_success'),
        cancel_url=domain + reverse('checkout_cancelled')
    )

    return render(request, "checkout/checkout.template.html", {
        'session_id': session.id,
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


def checkout_success(request):
    # Empty the shopping cart
    request.session['shopping_cart'] = {}
    return render(request, "checkout/payment_success.template.html")


def checkout_cancelled(request):
    return render(request, "checkout/checkout_cancelled.template.html")


@csrf_exempt
def payment_completed(request):
    # 1. verify that the data is actually sent by Stripe
    endpoint_secret = settings.ENDPOINT_SECRET
    payload = request.body
    # retrieve the signature
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Signature is invalid
        print("Invalid signature")
        return HttpResponse(status=400)

    # 2. process the order
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_payment(session)

    return HttpResponse(status=200)


def handle_payment(session):
    metadata = session['metadata']
    user = get_object_or_404(User, pk=session['client_reference_id'])
    all_listing_ids = json.loads(metadata['all_listing_ids'])
    for order_item in all_listing_ids:
        listing_model = get_object_or_404(Listing, pk=order_item['listing_id'])

        # Create the purchase model and save it manually
        purchase = Purchase()
        purchase.listing = listing_model
        purchase.user = user
        purchase.qty = order_item['qty']
        purchase.price = listing_model.price

        # remember to save the model
        purchase.save()
