from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django import forms
import random

from .forms import NewListingForm, NewBidForm, CommentForm
from .models import User, Auction, WatchList, Bid, Comment



def index(request):
    trendings = sorted(Auction.objects.annotate(num_bids=Count('active_bids')).order_by('-num_bids')[:8], key=lambda x: random.random())

    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all(),
        "trendings": trendings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def add_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/add_listing.html", {
        "form": NewListingForm()
    })

@login_required
def listing_page(request, listing_id):
    watched_by_user = WatchList.objects.filter(author=request.user, Product_Name_id=listing_id)
    page = Auction.objects.get(pk=listing_id)
    listing_author = page.author
    bids = Bid.objects.filter(Product_Name=listing_id)
    comments = Comment.objects.filter(Product_Name=listing_id)
    n_comments = len(comments)

    if len(bids) == 0:
        max_bid = "No Bid has been made yet on this Listing"
        winner = False
    else:
        max_bid = bids.aggregate(Max('Amount'))['Amount__max']
        winner_id = Bid.objects.filter(Amount=max_bid).values('BidAuthor')[0]['BidAuthor']
        winner = User.objects.get(pk=winner_id)

    bidform = NewBidForm(initial = {
        "Product_Name": page,
        "BidAuthor": request.user
    })

    commentform = CommentForm(initial = {
        "Product_Name": page,
        "made_by": request.user
    })

    if len(watched_by_user) == 0:
        watch_button_name = " Add to watchlist"
        icon_color = " color: Grey;"
    else:
        watch_button_name = "  Remove from watchlist"
        icon_color = "Dodgerblue"

    if page.listing_status == 'cl':
        close_button_status = "disabled"
        close_button_class = "not-allowed"
        close_button_text = "Auction is closed"
        
        if winner == request.user:
            display_winner = True
        else:
            display_winner = False
    else:
        close_button_status = ""
        close_button_class = ""
        close_button_text = "Close Auction"
        display_winner = False

    if page.author != request.user:
        show_close_button = False
    else:
        show_close_button = True
    
    if request.method == "GET":
        if page is not None:
            return render(request, "auctions/listing_page.html", {
                "page": page,
                "max_bid": max_bid,
                "winner": winner,
                "display_winner": display_winner,
                "button_name": watch_button_name,
                "button_status": close_button_status,
                "button_class": close_button_class,
                "close_button_text": close_button_text,
                "show_button": show_close_button,
                "icon_color": icon_color,
                "bidform": bidform, 
                "commentform": commentform,
                "comments": comments,
                "n_comments": n_comments
            })

    if request.method == "POST" and 'bid' in request.POST:
        
        if listing_author != request.user:
            bidform = NewBidForm(request.POST or None)
            
            if bidform.is_valid():
                bidform.save()
                return redirect('auctions:listing_page', listing_id)
        else:
            messages.warning(request, "You cannot bid  on your own listing!")
            return redirect('auctions:listing_page', listing_id)

    elif request.method == "POST" and 'comment' in request.POST:

        commentform = CommentForm(request.POST or None)
            
        if commentform.is_valid():
            commentform.save()
            return redirect('auctions:listing_page', listing_id)
        else:
            messages.warning(request,'Form is not valid!')
            return redirect('auctions:listing_page', listing_id)
        
    return render(request, "auctions/listing_page.html", {
                "page": page,
                "bidform": bidform,
                "commentform": commentform
            })


@login_required
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        page = get_object_or_404(Auction, pk=listing_id)
        if page.author != request.user:
            new_watch, created = WatchList.objects.get_or_create(author=request.user, Product_Name_id=listing_id)
            if not created:
                watched = WatchList.objects.get(author=request.user, Product_Name_id=listing_id)
                watched.delete()
                #messages.warning(request,'The item has been removed successfully!')
                return redirect('auctions:listing_page', listing_id)
            else:
                #messages.success(request,'The item was added to your watchlist!')
                return redirect('auctions:listing_page', listing_id)
        else:
            messages.warning(request, "Cannot add your own listing to your watchlist!")
            return redirect('auctions:listing_page', listing_id)


@login_required
def watchlist_page(request):
    watched_list = WatchList.objects.filter(author=request.user)
    nb_items = len(watched_list)
    
    if request.method == "GET":
        if nb_items == 0:
            no_item = True
        else:
            no_item = False

        return render(request, "auctions/watchlist.html", {
            "watched_list": watched_list,
            "no_item": no_item
        })



@login_required
def close_listing(request, listing_id):
    if request.method == "POST":
        page = Auction.objects.get(pk=listing_id)
        if page.author == request.user:
            page.listing_status = 'cl'
            page.save()
            return redirect('auctions:listing_page', listing_id)
        else:
            messages.error(request, "here we go again!")
            return redirect('auctions:listing_page', listing_id)

                   
@login_required
def get_categories(request):
    listings = Auction.objects.annotate(num_bids=Count('active_bids')).order_by('num_bids')[:8]
    labs = dict(Auction.ProductCategory.choices)
    
    categories = Auction.objects.order_by('product_cat').values("product_cat", 'category_image_url').distinct()
    
    categories = [{k: labs.get(v, v) for k, v in categories[i].items()}  for i in range(len(categories))]

    if request.method == 'GET':
        return render(request, 'auctions/categories.html', {
            "categories": categories,
            "listings": listings
        })


@login_required
def get_category_listings(request, category):
    if request.method == 'GET':
        labs = dict(Auction.ProductCategory.choices)
        try:
            category = [k for k, v in labs.items() if category == v][0]
        except IndexError:
            category = None

        listings = Auction.objects.filter(product_cat=category)

        return render(request, "auctions/category_listings.html", {
        "listings": listings
        })
