from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["starting_bid"]
        category = request.POST["category"]
        image_url = request.POST.get("image_url", "")
        # Here you would typically save the listing to the database
        # For now, we just render a success message
        if not title or not description or not price:
            return render(request, "auctions/new_listing.html", {
                "message": "All fields are required."
            })
        listing = Listing(
            title=title,
            description=description,
            price=price,
            owner=request.user,
            category=category,
            image_url=image_url if image_url else None
        )
        listing.save()

        return render(request, "auctions/index.html", {
            "message": "Listing created successfully!",
            "listings": Listing.objects.all()
        })
    else:
        return render(request, "auctions/new_listing.html")

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Listing not found."
        })

    comments = listing.comments.all()
    bids = listing.bids.all()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "bids": bids
    })

def watchlist(request):
    if request.user.is_authenticated:
        watchlist_items = request.user.watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist_items
        })
    else:
        return render(request, "auctions/login.html", {
            "message": "You must be logged in to view your watchlist."
        })

def like(request, listing_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "You must be logged in to like a listing."
        })

    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Listing not found."
        })

    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
        message = "Removed from watchlist."
    else:
        request.user.watchlist.add(listing)
        message = "Added to watchlist."

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def bid(request, listing_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "You must be logged in to place a bid."
        })

    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Listing not found."
        })

    if request.method == "POST":
        bid_amount = request.POST["amount"]
        if not bid_amount or float(bid_amount) <= listing.price:
            return render(request, "auctions/error.html", {
                "message": "Bid amount must be greater than the current price."
            })

        bid = Bid(listing=listing, user=request.user, amount=bid_amount)
        bid.save()

        listing.price = bid_amount
        listing.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/listing.html", {
        "listing": listing
    })

def close_listing(request, listing_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "You must be logged in to close a listing."
        })

    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Listing not found."
        })

    if listing.owner != request.user:
        return render(request, "auctions/error.html", {
            "message": "You are not the owner of this listing."
        })

    listing.is_active = False
    highest_bid = listing.bids.order_by('-amount').first()
    if highest_bid:
        listing.winner = highest_bid.user
    listing.save()

    return redirect("index")

def comment(request, listing_id):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
            "message": "You must be logged in to comment."
        })

    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message": "Listing not found."
        })

    if request.method == "POST":
        content = request.POST["comment"]
        if not content:
            return render(request, "auctions/error.html", {
                "message": "Comment cannot be empty."
            })

        comment = Comment(listing=listing, user=request.user, content=content)
        comment.save()

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/listing.html", {
        "listing": listing
    })

def categories(request):
    categories = Listing.objects.values_list('category', flat=True).distinct()

    if not categories:
        return render(request, "auctions/error.html", {
            "message": "No categories found."
        })

    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def category_listings(request, category_name):
    listings = Listing.objects.filter(category=category_name, is_active=True)

    if not listings:
        return render(request, "auctions/error.html", {
            "message": f"No listings found in category '{category_name}'."
        })

    return render(request, "auctions/category_listings.html", {
        "listings": listings,
        "category_name": category_name
    })