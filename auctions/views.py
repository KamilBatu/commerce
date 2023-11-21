from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category
from .models import User,Category,Listing, Comment, Bid
from django.contrib.auth.decorators import login_required



def create_listing(request):
    if request.method =='GET':
        category=Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            'category': category  
        })
    else:
        if request.method=='POST':
            title=request.POST['title']
            description=request.POST['description']
            imageurl=request.POST['imageurl']
            price=request.POST['price']
            category=request.POST['category']
            owner = request.user            
            categorydata=Category.objects.get(category_name=category)
            bid=Bid(bid=int(price), user=owner)
            bid.save()
            
            listingobject = Listing(
                        title=title,
                        description=description,
                        imageurl=imageurl,
                        price=bid,
                        user=owner,
                        category=categorydata,
                    )
            listingobject.save()
            return HttpResponseRedirect(reverse('index'))
  
        
def listing_page(request, id):
    list_item=Listing.objects.get(pk=id)
    is_in_watchlist=request.user in list_item.watchlist.all()
    allcomments=Comment.objects.filter(listing=list_item)
    isOwner=request.user.username==list_item.user.username
    return render(request, 'auctions/listing_page.html',
                  {'list_data': list_item,                                   
                    'is_in_watchlist': is_in_watchlist,
                    'allcomments':allcomments,
                    'isowner':isOwner
                    })


def addbid(request, id):
    newbid = request.GET.get('price')  # Use request.GET to access form data
   
    listingdata = Listing.objects.get(pk=id)
    is_in_watchlist=request.user in listingdata.watchlist.all()
    allcomments=Comment.objects.filter(listing=listingdata)
    isOwner=request.user.username==listingdata.user.username

    if newbid is not None:
        if int(newbid) > listingdata.price.bid:
            updateBid = Bid(user=request.user, bid=newbid)
            updateBid.save()
            listingdata.price = updateBid
            listingdata.save()
            return render(request, 'auctions/listing_page.html', {
                'list_data': listingdata,
                'message': 'Bid updated successfully',
                'update': True,
                'is_in_watchlist': is_in_watchlist,
                'allcomments':allcomments,
                'isowner':isOwner

            })
        else:
            return render(request, 'auctions/listing_page.html', {
                'list_data': listingdata,
                'message': 'Bid update failed',
                'update': False,
                 'is_in_watchlist': is_in_watchlist,
                'allcomments':allcomments,
                'isowner':isOwner

            })
    else:
        # Handle the case when 'price' parameter is missing from the request
        return render(request, 'auctions/listing_page.html', {
            'list_data': listingdata,
            'message': 'Bid update failed',
            'update': False,
            'isowner':isOwner

        })
 
def closebid(request, id):
    listingdata = Listing.objects.get(pk=id)
    listingdata.is_active=False
    listingdata.save()
    is_in_watchlist=request.user in listingdata.watchlist.all()
    allcomments=Comment.objects.filter(listing=listingdata)
    isOwner=request.user.username==listingdata.user.username
    return render(request, 'auctions/listing_page.html', {
                'list_data': listingdata,
                'message': 'Bid closed successfully',
                'update': True,
                'is_in_watchlist': is_in_watchlist,
                'allcomments':allcomments,
                 'isowner':isOwner

            })
    
    
    
def comment(request, id):
    author=request.user
    listing=Listing.objects.get(id=id)
    message=request.POST['newcomment']
    newMessage=Comment(author=author, listing=listing , message=message)
    newMessage.save()
    return HttpResponseRedirect(reverse('listing_page', args=(id,)));

def watchlist(request):
    c_user = request.user
    active_listing = c_user.watch_list.all()
    return render(request, 'auctions/watchlist.html', {'active_listing': active_listing})


def add_watchlist(request, id):
    data=Listing.objects.get(pk=id)
    c_user=request.user
    data.watchlist.add(c_user)
    return HttpResponseRedirect(reverse('listing_page', args=(id,)));


def remove_watchlist(request, id):
    data=Listing.objects.get(pk=id)
    c_user=request.user
    data.watchlist.remove(c_user)
    return HttpResponseRedirect(reverse('listing_page', args=(id,)));


def index(request):
    category=Category.objects.all()
    active_listing = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {'active_listing': active_listing, 
                            'category': category })


def category(request):
    category=Category.objects.all()
    active_listing = Listing.objects.filter(is_active=True)
    return render(request, "auctions/categories.html", {'active_listing': active_listing, 
                            'category': category })
    
    
def selected_category(request):
    if request.method == 'POST':  
        select_category = request.POST['selected_category']
        get_category = Category.objects.get(category_name=select_category)
        active_listing = Listing.objects.filter(is_active=True, category=get_category)
        category = Category.objects.all()
        
        return render(request, "auctions/index.html", {'active_listing': active_listing, 
                                'category': category })

        


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
