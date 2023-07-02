import stripe
import os

SECRET_KEY = os.environ.get('stripe_key')
stripe.api_key=SECRET_KEY

def generate_card_token(cardnumber,expmonth,expyear,cvv):
    data= stripe.Token.create(
            card={
                "number": str(cardnumber),
                "exp_month": int(expmonth),
                "exp_year": int(expyear),
                "cvc": str(cvv),
            })
    card_token = data['id']

    return card_token


def create_payment_charge(tokenid,amount,description):
    payment = stripe.Charge.create(
                amount= int(amount)*100,                  # convert amount to cents
                currency='eur',
                description=description,
                source=tokenid,
                )
    payment_check = payment['paid']    # return True for successfull payment
    return payment_check

if __name__=='__main__':
    print(os.environ.get("stripe_key"), 'got key')
    gen_card=generate_card_token( 4242424242424242,12,34,233)
    print(gen_card)
    a=create_payment_charge(gen_card,100,'test')
    print(a)