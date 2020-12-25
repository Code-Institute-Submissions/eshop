from django import forms
from .models import Listing
from cloudinary.forms import CloudinaryJsFileField

class ListingForm(forms.ModelForm):
    price = forms.IntegerField(label='Price (In Cents)')
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'price', 'seller', 'cover']
    cover = CloudinaryJsFileField()


