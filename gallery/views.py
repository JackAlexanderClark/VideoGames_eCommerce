from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import VideoGame
from shipping.models import Order, UserShippingDetails, Card,Receipt
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from gallery.stripe_methods import generate_card_token, create_payment_charge
from ast import literal_eval
from .models import EditProfileForm
import json
import stripe
import os
import stripe.error

SECRET_KEY = os.environ.get('stripe_key')
stripe.api_key=SECRET_KEY

# Create your views here.
from django.contrib import messages

def home(request):

    return render(request, 'html/home.html')



def profile(request):
    # handle receipts for each user
    receipts=Receipt.objects.filter(user_id=request.user).all()
    receipts=list(receipts)
    receipts.sort(key=lambda a: -a.receipt_id)
    for receipt in receipts:
        receipt.items=literal_eval(receipt.items)
    context={
        'receipts':receipts
    }
    return render(request, 'html/profile.html',context=context)

def gallery(request):

    games=VideoGame.objects.all()
    context={
        "images":games
    }
    return render(request, 'html/gallery.html',context=context)


def logout_view(request):

    logout(request)
    return redirect('home')


def login_view(request):

    message=''
    context={
        'message':message
    }
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request,username=username,password=password)
        print(user)
        if user:
            login(request,user)
            context['message'] = 'Logged In'
            return redirect('home')
        else:
            context['message'] = 'Invalid credentials'
            return render(request, 'html/login.html',context=context)
    return render(request, 'html/login.html',context=context)

def register_view(request):

    message = 'user registered'
    context = {
        'message': message
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password == password2:
            old_user = User.objects.filter(username=username).first()
            if not old_user:
                new_user = User()
                new_user.username=username
                new_user.set_password(password)
                new_user.email = email
                new_user.save()
                messages.success(request, 'New user created: '+username)

                login(request, new_user)
                messages.success(request, 'Logged In: ' + username)
            else:
                messages.error(request, 'User already exists')
        else:
            messages.error(request, 'Passwords dont match')

        return redirect('home')

    return render(request, 'html/register.html', context=context)


def video(request, id):

    game = VideoGame.objects.filter(video_game_id=id).first()
    if request.method == 'POST':
        # this is error
        User=request.user
        delivery_cost = game.price
        olduser=Order.objects.filter(user_id=User,game_id__video_game_id=game.video_game_id).first()
        if olduser:
            print("user exist")
            olduser.quantity += 1
            olduser.save()
            messages.add_message(request, messages.SUCCESS, "Added :"+game.name)
        else:
            newOrder = Order(user_id=User, game_id=game, delivery_cost=delivery_cost,
                           delivery_option='slow')
            newOrder.save()
            messages.add_message(request,messages.SUCCESS, "Added to Card.")
        return redirect('cart')

    return render(request,'html/video.html', context={"game":game})


@csrf_exempt
def remove_game_item(request,id):

    # remove one from cart item when http sent from javascript
    if (request.method == 'POST'):
        game=Order.objects.get(order_id=id)
        print(game.quantity)
        if game.quantity > 0:
            game.quantity -= 1
            game.save()
            return JsonResponse({"success": True}, status=200)
        else:

            return JsonResponse({"success": False}, status=400)
    return JsonResponse({"error": ""}, status=400)

@csrf_exempt
def add_game_item(request,id):

    # remove one from cart item when http sent from javascript
    if (request.method == 'POST'):
        game=Order.objects.get(order_id=id)
        print(game.quantity)
        if game.quantity <5:
            game.quantity += 1
            game.save()
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"message": "Upper limited reached"}, status=400)
    return JsonResponse({"error": "Internal server error"}, status=400)

@csrf_exempt
def delete_game_item(request,id):

    # remove one from cart item when http sent from javascript
    if (request.method == 'POST'):
        game=Order.objects.get(order_id=id)

        print(game.quantity)
        if game:
            game.delete()
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse({"success": False}, status=400)
    return JsonResponse({"error": ""}, status=400)


def load_edit_profile(request):

    return render(request, 'html/editprofile.html')


def edit_profile(request):
    # update user info for profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exclude(username=request.user.username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('edit_profile')

            user = form.save()
            return redirect('profile')

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'html/editprofile.html', {'form': form})


