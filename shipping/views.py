from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from gallery.models import VideoGame
from .models import Order, UserShippingDetails, Card, Receipt
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from gallery.stripe_methods import generate_card_token, create_payment_charge
from ast import literal_eval
from django.contrib import messages
import json
import stripe
import os

SECRET_KEY = os.environ.get('stripe_key')
stripe.api_key = SECRET_KEY

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
        return render(request, 'shipping/templates/html/buy.html', context=context)
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
                messages.error(request,"checkpoint 1 "+str(e))
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
                    messages.error(request,"checkpoint 2 "+str(e))
                if is_card_valid:
                    details.save()
                else:
                    status=False
                    # give error to user payment failed
                    messages.error(request,'Invalid Card Details - Payment Failed')
                print('POST name: ',request.POST,type(request.POST),"end")
            except Exception as e:
                status=False
                messages.error(request,"checkpoint 3 "+str(e))
            if status:
                messages.success(request,'Details Added Successfully')
                return redirect("receipt")
            messages.error(request,"Fill Details again")
            return redirect('buy')


def cart(request):

    user_id=request.user
    if request.user.is_authenticated:

        orders=Order.objects.filter(user_id=user_id)
        context={"orders":orders}
        return render(request, 'shipping/templates/html/cart.html', context=context)
    messages.info(request,'Login Required for Cart')
    return redirect('home')


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
        return render(request, 'shipping/templates/html/receipt.html', context=context)

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