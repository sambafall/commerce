from django import forms
from django.db.models import Max

from .models import Auction, Bid, Comment



class NewListingForm(forms.ModelForm):
    class Meta:
        model = Auction
        exclude = ('author', 'listing_status')

        labels = {
             "product_name": "Listing Title",
             "product_cat": "Listing category",
             "minimal_bid": "Starting Bid",
             "description": "Description",
             "product_image_url": "Listing Image URL",
             "category_image_url": "Listing Category Image URL"
             }
        
        widgets = {
            "product_name": forms.TextInput(attrs={'class': 'form-control'}),
            "product_cat": forms.Select( attrs={'class': 'form-control'}),
            "minimal_bid": forms.NumberInput(attrs={'class': 'form-control'}),
            "description":  forms.Textarea(attrs={'class': 'form-control'}),
            "product_image_url": forms.URLInput(attrs={'class': 'form-control'}),
            "category_image_url": forms.URLInput(attrs={'class': 'form-control'})
        }
        

class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('Amount', 'Product_Name')

        labels = {
        'Amount': '',
    }

        widgets = {
            "Amount": forms.NumberInput(attrs={'class': 'form-control'}),
            "Product_Name": forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        listing_id = self.cleaned_data['Product_Name'].id
        amount = cleaned_data.get('Amount')
        starting_bid = cleaned_data.get('Product_Name').minimal_bid
        bids = Bid.objects.filter(Product_Name=listing_id)
        max_bid = bids.aggregate(Max('Amount'))['Amount__max']
        if not max_bid:
            if amount < starting_bid:
                raise forms.ValidationError('Bid amount must be greater or equal than the starting bid')
            return self.cleaned_data
        else:
            if amount < starting_bid or amount <= max_bid:
                raise forms.ValidationError('Bid must be 1: \n greater or equal than the starting bid, \n 2: greater than the current highest bid')
            return self.cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

        labels = {
             "title": "Comment Title",
             "Content": "Content"
             }
        
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "Content":  forms.Textarea(attrs={'class': 'form-control'}),
             "Product_Name": forms.HiddenInput(),
             "made_by": forms.HiddenInput(),
             "Comment_Date": forms.HiddenInput()
            }

