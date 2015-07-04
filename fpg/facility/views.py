from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import stripe

# # Create your views here.
# from django.views.decorators.csrf import csrf_exempt
#
#
#
# @csrf_exempt
# def payment_callback_view(request):
#     stripe.api_key = "sk_test_QBpIvo5lNrftaWto9c9hYrKY"
#     import ipdb;ipdb.set_trace()
#     # Get the credit card details submitted by the form
#
#     token = request.POST['stripeToken']
#
#
#     # Create the charge on Stripe's servers - this will charge the user's card
#
#     try:
#         charge = stripe.Charge.create(
#           amount=1000, # amount in cents, again
#           currency="usd",
#           source=token,
#           description="Example charge"
#         )
#
#
#     except stripe.error.CardError, e:
#         # The card has been declined
#         pass
#
#     return HttpResponseRedirect('/#/result??')