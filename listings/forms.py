from django import forms
from .models import Listing, Category
from cloudinary.forms import CloudinaryJsFileField


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'price', 'cover']
    price = forms.IntegerField(label='Price (In Cents)')
    cover = CloudinaryJsFileField(
        label='Product Image (square img recommended)')


class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False)
