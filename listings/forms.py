from django import forms
from .models import Listing
from cloudinary.forms import CloudinaryJsFileField

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'price', 'cover']
    price = forms.IntegerField(label='Price (In Cents)')
    cover = CloudinaryJsFileField(label='Product Image (square img recommended)')


