from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid



def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    comments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request,"auctions/listing.html",{
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": comments,
        "isOwner" : isOwner
    } )


def endAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    comments = Comment.objects.filter(listing=listingData)
    
    return render(request,"auctions/listing.html",{
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": comments,
        "isOwner" : isOwner,
        "update" : True,
        "message" : "Congratulations! Your item is sold."
    } )



def removeFromWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse('listing', args=(id, )))
    
def addFromWatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser) # watchlist IS a field
    return HttpResponseRedirect(reverse('listing', args=(id, )))

def watchlist(request):
    currentUser = request.user
    listings = currentUser.watchlistt.all()

    return render(request, "auctions/watchlist.html", {
        "listings" : listings,
   
    })


def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['comment']
    comment = Comment(
        author = currentUser,
        listing = listingData,
        message = message
    )
    comment.save()

    return HttpResponseRedirect(reverse("listing",args=(id, )))

def addBid(request, id):
    newBid = int(request.POST['bid'])
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    comments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username

    if newBid > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=newBid)
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message" : "Bid was Updated",
            "update": True,
            "isListingInWatchlist": isListingInWatchlist,
            "comments": comments,
            "isOwner" : isOwner
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message" : "Bid wasn't Updated",
            "update": False,
            "isListingInWatchlist": isListingInWatchlist,
            "comments": comments,
            "isOwner" : isOwner
        })


def index(request):
    active_listing = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":active_listing,
        "categories": categories
    })

def categoryPage(request):
    category = request.POST["category"]
    category = Category.objects.get(categoryName=category)
    if request.method == "POST":
        active_listing = Listing.objects.filter(isActive=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings":active_listing,
            "categories": categories
        })
    
def add_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/add.html", {
            "categories" : categories
        })
    else:
        #get form data
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
       
        currentuser = request.user
        category_data = Category.objects.get(categoryName=category)
        #create bid obj
        bid = Bid(bid=float(price), user=currentuser)
        bid.save()

        new_listing = Listing(
            title=title,
            description=description,
            imageUrl = imageurl,
            price = bid,
            category = category_data,
            owner = currentuser
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))

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
