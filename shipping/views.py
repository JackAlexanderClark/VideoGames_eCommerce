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
        return render(request, 'html/buy.html', context=context)
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
        return render(request, 'html/cart.html', context=context)
    messages.info(request,'Login Required for Cart')
    return redirect('home')

