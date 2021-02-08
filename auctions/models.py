from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import URLValidator
from django.db import models
from crum import get_current_user
from django.conf import settings
import datetime



class User(AbstractUser):
    pass


class Auction(models.Model):
    class ProductCategory(models.TextChoices):
        App_Acc = 'AA', _('Apparel and Accessories')
        Sty_Fash = 'SF', _('Style and Fashion')
        Hom_Gar = 'HG', _('Home and Garden')
        Spor_Goo = 'SG', _('Sporting and Goods')
        Health_Well = 'HW', _('Health and Wellness')
        Child_Infan = 'CI', _('Children and Infants')
        Electronic = 'EG', _('Electronic Goods')
        Home = 'HO', _('Home')
        Auto = 'AU', _('Automotive')
        Oth_Cat = 'OC', _('Other Categories')
        Not_Kwn = 'NK', _('Not Known')

    class ListingStatus(models.TextChoices):
        active = 'ac', _("Active")
        closed = 'cl', _("Closed")

    product_cat = models.CharField(max_length=2, choices=ProductCategory.choices, default=ProductCategory.Not_Kwn,)
    listing_status = models.CharField(max_length=2, choices=ListingStatus.choices, default=ListingStatus.active,)
    product_name = models.CharField(max_length=64)
    minimal_bid = models.DecimalField(max_digits=19, decimal_places=2)
    description =  models.TextField(blank=True)
    product_image_url = models.URLField(max_length=250, blank=True, validators=[URLValidator()])
    category_image_url = models.URLField(max_length=250, blank=True, validators=[URLValidator()])
    pubdate = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user, on_delete=models.CASCADE, blank=True, related_name="listings")
    

    def __str__(self):
        return f"{self.id}: {self.product_name}, Starting bid: {self.minimal_bid}, Status:{self.listing_status}, category: {self.product_cat}"


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Auction, self).save(*args, **kwargs)

class Bid(models.Model):
    Product_Name = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="active_bids")
    Amount = models.DecimalField(max_digits=19, decimal_places=2)
    BidDate = models.DateTimeField(auto_now_add=True, blank=True)
    BidAuthor = models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user, on_delete=models.CASCADE, blank=True, related_name="bids")

    def __str__(self):
        return f"{self.Product_Name} {self.Amount} {self.BidAuthor} {self.BidDate}"

    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Bid, self).save(*args, **kwargs)


class WatchList(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user, on_delete=models.CASCADE, blank=True, related_name="followed_listings")
    Product_Name = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, related_name="likes")
    added_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.Product_Name}, {self.added_at}"


class Comment(models.Model):
    made_by =  models.ForeignKey(settings.AUTH_USER_MODEL, default=get_current_user, on_delete=models.CASCADE, blank=True, related_name="comments")
    Product_Name = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="Comments")
    title = models.CharField(max_length=200)
    Comment_Date = models.DateTimeField(blank=True, default=timezone.localtime)
    Content = models.TextField(blank=True)

    def __str__(self):
            return f"{self.title}: \n {self.Content}"

