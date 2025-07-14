from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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