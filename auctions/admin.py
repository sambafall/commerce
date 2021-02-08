from django import forms
from django.contrib import admin
from django.db.models import Max
from .models import User, Auction, Bid, Comment, WatchList


# Register your models here.
class BidAdminForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'

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
                raise forms.ValidationError('Bid must be 1: greater or equal than the starting bid, 2: greater than the current highest bid')
            return self.cleaned_data



class BidAdmin(admin.ModelAdmin):
    form = BidAdminForm
    list_display = ("id", "Product_Name", "BidAuthor", "Amount", "BidDate")


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "product_name", "minimal_bid", "product_cat", "listing_status")


class CommentAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in Comment._meta.fields]


class WatchListAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in WatchList._meta.fields]

admin.site.register(User)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WatchList, WatchListAdmin) 