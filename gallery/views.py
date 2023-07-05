from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import VideoGame
from shipping.models import Order, UserShippingDetails, Card,Receipt
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from gallery.stripe_methods import generate_card_token, create_payment_charge
from ast import literal_eval
# from .forms import UpdateProfileForm
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

def cart(request):

    user_id=request.user
    if request.user.is_authenticated:

        orders=Order.objects.filter(user_id=user_id)
        context={"orders":orders}
        return render(request,'html/cart.html',context=context)
    messages.info(request,'Login Required for Cart')
    return redirect('home')

def buy(request):
    # select the card
    # get address
    if request.method=='GET':
        shippingDetails=UserShippingDetails.objects.filter(user_id=request.user).all()
        cardDetails=Card.objects.filter(user_id=request.user).all()
        print(bool(shippingDetails),bool(cardDetails))

        if shippingDetails:
            shippingDetails=shippingDetails.first()
            getShippingDetails=False
        else:
            getShippingDetails=True

        if cardDetails:
            cardDetails = cardDetails.first()
            getcardDetails = False
        else:
            getcardDetails = True
        receipt={
            'total_amount':0,
            'receipt_id':Receipt.objects.count()+1,
            'items':{

            },
            'tax':0
        }
        #calc total amount
        receipt['tax']=receipt['total_amount']/10
        receipt['total_amount']+=receipt['tax']
        context={
            'shippingDetails':shippingDetails,
            'getShippingDetails':getShippingDetails,
            'cardDetails':cardDetails,
            'getCardDetails':getcardDetails,
            'receipt':receipt
        }
        return render(request,'html/buy.html',context=context)
    else:
        if request.POST['form']=='msform':
            status=True
            try:
                details=UserShippingDetails.objects.filter(user_id=request.user)
                if details:
                    details=details.first()
                else:
                    details = UserShippingDetails()
                    details.user_id=request.user
                details.address_line=request.POST['address']
                details.postcode=request.POST['postcode']

                details.phone_number=request.POST['number']
                details.speed=request.POST['shipping_speed']
                details.country=request.POST['country']
                details.save()

            except Exception as e:
                status=False
                messages.error(request,str(e))
            try:
                details=Card.objects.filter(user_id=request.user)
                if details:
                    details=details.first()
                else:
                    details = Card()
                    details.user_id=request.user
                details.card_number=request.POST['card_number']
                details.exp_month=request.POST['exp_month']

                details.exp_year=request.POST['exp_year']

                details.cvc=request.POST['cvc']

                is_card_valid=None
                try:
                    is_card_valid=generate_card_token(stripe, details.card_number, details.exp_month, details.exp_year, details.cvc)
                except Exception as e:
                    messages.error(request,str(e))

                if is_card_valid:
                    details.save()
                else:
                    status=False
                    messages.error(request,'Invalid Card Details')
                print('POST name: ',request.POST,type(request.POST),"end")
            except Exception as e:
                status=False
                messages.error(request,str(e))
            if status:
                messages.success(request,'Details Added Successfully')
                return redirect("receipt")
            messages.error(request,"Fill Details again")
            return redirect('buy')

    # button

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

    return render(request, 'html/register.html', context='context')


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
            messages.add_message(request, messages.SUCCESS, "Added one more :"+game.name)
        else:
            newOrder = Order(user_id=User, game_id=game, delivery_cost=delivery_cost,
                           delivery_option='slow')
            newOrder.save()
            messages.add_message(request,messages.SUCCESS, "Added to Card.")
        return redirect('cart')

    return render(request,'html/video.html', context={"game":game})

def receipt(request):

    if request.method=='GET':
        # load receipt object generated on purchase
        user=request.user
        context={
            'total_amount':0,
            'receipt_id':0,
            'items':"",
            'tax':0
        }
        items = []
        user_id = request.user
        orders = Order.objects.filter(user_id=user_id)
        total_amount = 0
        if not orders:
            messages.info(request,'Cart Empty')
            return redirect('cart')
        for order in orders:
            item_price = order.game_id.price
            items.append([
                order.order_id,
                order.game_id,
                item_price,
                order.quantity,
                order.delivery_cost,
                str(order.is_processed)
                ])
            total_amount += item_price
        tax = 0.05 * total_amount
        context['total_amount']=total_amount
        context['receipt_id']='Preview'
        context['items']= items
        context['tax']=tax
        context['delivery_option']=order.delivery_option

        # get the card
        # get the address
        shippingDetails = UserShippingDetails.objects.filter(user_id=request.user).all()
        cardDetails = Card.objects.filter(user_id=request.user).all()
        context['shipping'] = shippingDetails
        context['card'] = cardDetails
        if shippingDetails and cardDetails:
            pass
        else:
            redirect('buy')
        return render(request, 'html/receipt.html',context=context)

    if request.method == 'POST':
        if request.POST['button'] == 'confirm':
            items = []
            user_id = request.user
            orders = Order.objects.filter(user_id=user_id)
            if not orders:
                messages.info(request, 'Cart Empty')
                return redirect('cart')
            total_amount = 0
            print(orders)
            for order in orders:
                item_price = order.game_id.price
                items.append([
                    order.order_id,
                    order.game_id.name,
                    item_price,
                    order.quantity,
                    order.delivery_cost,
                    str(order.is_processed)
                ])
                total_amount += item_price
            tax = 0.05 * total_amount
            receipt = Receipt()
            receipt.user_id = request.user
            receipt.delivery_option = order.delivery_option
            receipt.total_amount = total_amount
            receipt.tax = tax

            receipt.items = json.dumps(items)
            receipt.save()
            for order in Order.objects.filter(user_id=request.user):
                order.delete()
            # handle error if card details are incorrect
            try:
                card = Card.objects.filter(user_id=request.user).first()
                charged = create_payment_charge(stripe, generate_card_token(stripe, card.card_number, card.exp_month,
                                                                            card.exp_year, card.cvc), total_amount, 'VideoGames Payment')
                messages.success(request, str(charged))
                messages.success(request, "Order Placed Successfully, check your profile for a receipt and status.")
                return redirect('home')
            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.error(request, f"Payment failed: {err.get('message')}")
                return redirect('receipt')
        else:
            messages.info(request, 'Order Cancelled')
            # redirect to shop
            return redirect('home')
        return redirect('receipt')



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
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()

            # update password
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            update_session_auth_hash(request, form.user)  # Important!

            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


