from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
import stripe
import json
import os
from dotenv import load_dotenv
from products.models import Cart

# Create your views here.
load_dotenv()
stripe.api_key = os.getenv('SECRET_KEY')


def create_checkout_session(request):
    if request.method == 'POST': 
        try:
            print( "Initial---------", request.POST)
            # get_customer = stripe.Customer.search(query="email:'farad.alam@gmail.com'")

            cart_products = Cart.objects.filter(user=request.user).values()
            cart_product_list = list(cart_products)
            
            # Serialize cart_product_list to JSON
            serialized_cart_products = json.dumps(cart_product_list, cls=DjangoJSONEncoder)
            print(serialized_cart_products)

            subtotal = Cart.subtotal_product_price(request.user)
            amount = subtotal*100
         
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                # customer= customer,
                amount=int(amount),
                currency='usd',
                automatic_payment_methods={'enabled': True},
                metadata={'cart_products': serialized_cart_products},
            )

            print(intent.client_secret)
            print('paymentIntent===', intent)
            return JsonResponse({'clientSecret': intent.client_secret})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)


# Display Payment Details with products
def display_payment_details(request):
    cart_products = Cart.objects.filter(user=request.user)

    context = {
        'cart_products':cart_products,
        'payable': Cart.subtotal_product_price(request.user)
    }

    return render(request,'payments/payment.html', context)


from products.views import placed_oder

def payment_success(request):
    payment_intent_id= request.GET.get('payment_intent')
    email = request.user.email
    # print(email)
    # After make payment placed the oder
    oder_placed = placed_oder(request)
    get_customer = stripe.Customer.search(query=f'email:"{email}"')
    if get_customer:
        customer = get_customer['data'][0]
    else:                  
        customer = stripe.Customer.create(
            name= request.user.first_name,
            email=request.user.email,
            description="Creating user for purchasing product"
        )
        print(customer)

    # updating the wxisting payment intent
    payment_intent = stripe.PaymentIntent.modify(
        payment_intent_id,
        metadata = {'oder_id': oder_placed},
        customer = customer
       
    )
    print(payment_intent)
    amount_paid = payment_intent['amount_received'] / 100

    context = {
        "payment_intent":payment_intent,
        "amount_paid": amount_paid
    }

    return render(request,'payments/success.html',context)