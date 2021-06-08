from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from django.contrib.auth.decorators import login_required

from .models import User, List, Bid, WahchList, Comment
from django.db.models import Max, Sum
from django.contrib.auth.models import User

from .forms import BidForm, AddList, WahchListForm, TurnOff, CommentForm, CategoryForm


def index(request):
    active_li = List.objects.filter(active = True)

    bids = Bid.objects.all().values('item_id').annotate(Max('bid'))

    categories = CategoryForm()
    return render(request, "auctions/index.html", {
        "actives":active_li,
        "bids": bids,
        "categories":categories
    })


def category(request):
    if request.method == "POST":
        
        req = CategoryForm(request.POST)
        if req.is_valid():
            category = req.data.get('category')
            active_li = List.objects.filter(active = True, category=category)

            bids = Bid.objects.all().values('item_id').annotate(Max('bid'))
            return render(request, "auctions/category.html", {
                "category":category,
                "actives":active_li,
                "bids": bids,
            })
        else:
            category = "Can't Find Requested Category!"
            return render(request, "auctions/category.html", {
                "category":category,
                "actives":active_li,
                "bids": bids,
            })

    else:
        return HttpResponseRedirect(reverse('index'))


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


# ratom magdebs ??????????????????????????

@login_required
def watch_list(request):
    user_id = request.user.id
    watch =  WahchList.objects.filter(user_id = user_id)
    
    bids = Bid.objects.all().values('item_id',"user_id").annotate(Max('bid'))

    # watch_list = List.objects.filter(user_id = watch_li.user_id, item_id = watch_li.item_id)

    return render(request, "auctions/watch_list.html", {
        "watch_li": watch,
        "bids":bids,
        "current_user":user_id 
    })

@login_required
def add(request):
    if request.method == "POST":
        form = AddList(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("index"))


    user_id = request.user.id
    form = AddList(initial={"user_id":user_id})  
    return render(request, "auctions/add.html", {
        'forms': form,
    })

@login_required
def listing_page(request, item_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_id = request.user.id
            
            # if it is emty set None
            max_bid = (Bid.objects.filter(item_id = item_id).values('item_id',"user_id").annotate(Max('bid')) or None)

            form = BidForm()

            page = List.objects.get(item_id = item_id)

            if max_bid is None:
                MAX =  page.start_bid
            else:
                MAX = max_bid[0]["bid__max"]

            # For Adding To WhatchList:
            add_watch_list = WahchListForm(request.POST or None)
        
                
            # WahchListForm
            whatch_form = WahchListForm(initial={"user_id":user_id, "item_id":item_id})
            # check if it alreaddy added
            watch_list = WahchList.objects.filter(item_id = item_id, user_id = user_id)
            added = bool
            if not watch_list:
                added = False
            else:
                added = True

    # migrate info :
     # check if item is users's
            page_is_users = bool
            # to take users_id s primary key value
            if int(page.user_id.pk) == user_id:
                page_is_users = True
            else:
                page_is_users = False

            turn_off = TurnOff()

    # Comments:
            comments_form = CommentForm(request.POST or None)
            if comments_form is not None and comments_form.is_valid:
                try:
                    comments_form.save()

                    comments_form = CommentForm(initial={"user_id":user_id, "item_id":item_id,"name": request.user.username})
                    comments = (Comment.objects.all().filter(item_id=item_id).order_by('created_on') or None)
                    return render(request, "auctions/listing_page.html", {
                        "page":page,
                        'form': form,
                        "bid":max_bid,
                        "text": "You Comment Successfully",
                        "whatch_form":whatch_form,
                        "added": added,

                        "page_is_users":page_is_users,
                        "turn_off":turn_off,
                        "current_user":user_id,

                        "comments_form":comments_form,
                        'comments':comments
                        })
                except ValueError:
                    pass


            comments_form = CommentForm(initial={"user_id":user_id, "item_id":item_id, "name": request.user.username})

            comments = (Comment.objects.all().filter(item_id=item_id).order_by('created_on') or None)


            #    # For BID
            form = BidForm(request.POST or None)
            if form.is_valid():
                bid = int(form['bid'].value())
            # for Bid and initial values:
                if  MAX < bid:
                    form.save()
                    # new value of max_bid
                    max_bid = max_bid = Bid.objects.filter(item_id = item_id).values('item_id',"user_id").annotate(Max('bid')) 
                    return render(request, "auctions/listing_page.html", {
                    "page":page,
                    'form': form,
                    "bid":max_bid,
                    "text": "You Bid Successfully",
                    "whatch_form":whatch_form,
                    "added": added,

                    "page_is_users":page_is_users,
                    "turn_off":turn_off,
                    "current_user":user_id,

                    "comments_form":comments_form,
                    'comments':comments
                    })
                if MAX >= bid:
                    max_bid = max_bid = Bid.objects.filter(item_id = item_id).values('item_id',"user_id").annotate(Max('bid')) 
                    return render(request, "auctions/listing_page.html", {
                    "page":page,
                    'form': form,
                    "bid":max_bid,
                    "text": "Money is'not enough to Bid. SET More!",
                    "whatch_form":whatch_form,
                    "added": added,

                    "page_is_users":page_is_users,
                    "turn_off":turn_off,
                    "current_user":user_id,

                    "comments_form":comments_form,
                    'comments':comments
                    })


            
            form = BidForm(initial={"user_id":user_id, "item_id":item_id})
        # add Watch List:
            if added is False and add_watch_list.is_valid():
                add_watch_list.save()
                added = True
                return render(request, "auctions/listing_page.html", {
                "page":page,
                'form': form,
                "bid":max_bid,
                "text": "You Added item to Watchlist!",
                "whatch_form":whatch_form,
                "added": added,

                "page_is_users":page_is_users,
                "turn_off":turn_off,
                "current_user":user_id,

                "comments_form":comments_form,
                'comments':comments
                })

        #delete item from Watchlist: 
            if added is True and add_watch_list.is_valid():
                WahchList.objects.filter(user_id = user_id, item_id = item_id).delete()

                added = False
                return render(request, "auctions/listing_page.html", {
                "page":page,
                'form': form,
                "bid":max_bid,
                "text": "Item Deleted from Watchlist!",
                "whatch_form":whatch_form,
                "added": added,

                "page_is_users":page_is_users,
                "turn_off":turn_off,
                "current_user":user_id,

                "comments_form":comments_form,
                'comments':comments
                })

            
            if added is True:
                return render(request, "auctions/listing_page.html", {
                "page":page,
                'form': form,
                "bid":max_bid,
                "text": "You have already added item to Watchlist!",
                "whatch_form":whatch_form,
                "added": added,

                "page_is_users":page_is_users,
                "turn_off":turn_off,
                "current_user":user_id,

                "comments_form":comments_form,
                'comments':comments,
                })

            else:
                # all to render file:
                return render(request, "auctions/listing_page.html", {
                "page":page,
                'form': form,
                "bid":max_bid,
                "text": "Your Bid failed! SET More BID (Value)!",
                "whatch_form":whatch_form,
                "added": added,

                "page_is_users":page_is_users,
                "turn_off":turn_off,
                "current_user":user_id,

                "comments_form":comments_form,
                'comments':comments
                })
        

# if request is GET:
        else:
            user_id = request.user.id
            page = List.objects.get(item_id = item_id)

            max_bid = Bid.objects.filter(item_id = item_id).values('item_id',"user_id").annotate(Max('bid'))    
            # Define Forms and initial values:
            form = BidForm()
            turn_off = TurnOff()
           
            # initial value of:
            form = BidForm(initial={"user_id":user_id, "item_id":item_id})

            # WahchListForm
            whatch_form = WahchListForm(initial={"user_id":user_id, "item_id":item_id})
            # check if it alreaddy added
            watch_list = WahchList.objects.filter(item_id = item_id, user_id = user_id)
            added = bool
            if not watch_list:
                added = False
            else:
                added = True

            # check if item is users's
            page_is_users = bool
            # to take users_id s primary key value
            if int(page.user_id.pk) == user_id:
                page_is_users = True
            else:
                page_is_users = False


            # # Coments : 
            comments_form = CommentForm(initial={"user_id":user_id, "item_id":item_id, "name": request.user.username})

            comments = (Comment.objects.all().filter(item_id=item_id).order_by('created_on') or None)
            
            return render(request, "auctions/listing_page.html", {
                "page":page,
                'form': form,
                "bid":max_bid,
                "whatch_form":whatch_form,
                "added": added,
                "page_is_users":page_is_users,
                "turn_off":turn_off,
                "current_user":user_id,

                "comments_form":comments_form,
                'comments':comments
            })
    # if user is not loged in
    else:
        return render(request, "auctions/login.html", {
                "message": "You need to Log in!"
            })

@login_required
def turn_off(request, item_id):
    if request.method == 'POST':
        turn_off = TurnOff(request.POST or None)
    # gamortvis logika
        item = List.objects.get(item_id = item_id)
        if turn_off.is_valid:
            item.active = False
            item.save()
        return HttpResponseRedirect(reverse('listing_page', args=(item_id,)))
    # shechvale chemi listebis gverdi

    
    else: 
        return render(request, "auctions/turn.html", {
                "message":"ERROR IT's request.GET Not request.POST"
            })


@login_required
def my_items(request):
    user_id = request.user.id
    my_items = List.objects.filter(user_id = user_id)

    return render(request, "auctions/my_items.html", {
        "actives":my_items,
    })
