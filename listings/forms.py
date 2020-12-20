from django import forms
from .models import Listing
from cloudinary.forms import CloudinaryJsFileField

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'SKU', 'description', 'category', 'seller', 'cover')
    cover = CloudinaryJsFileField()