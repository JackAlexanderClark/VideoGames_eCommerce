# handles stripe API payment logic
import os
def generate_card_token(stripe,cardnumber,expmonth,expyear,cvv):
    data= stripe.Token.create(
            card={
                "number": str(cardnumber),
                "exp_month": int(expmonth),
                "exp_year": int(expyear),
                "cvc": str(cvv),
            })
    card_token = data['id']

    return card_token


def create_payment_charge(stripe,tokenid,amount,description):
    payment = stripe.Charge.create(
                # use game.amount var
                amount= int(amount)*100,
                currency='eur',
                description=description,
                source=tokenid,
                )
    payment_check = payment['paid']
    return payment_check

if __name__=='__main__':
    print(os.environ.get("stripe_key"), 'got key')
    a=create_payment_charge(generate_card_token(1234567812345678,11,29,233),100,'test')
    print(a)