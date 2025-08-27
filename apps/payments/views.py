from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
import json
import requests
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

CallbackURL = 'http://127.0.0.1:8080/payments/verify/'

class ZarinpalPaymentView(LoginRequiredMixin,View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            user = request.user
            req_data = {
                "MerchantID": MERCHANT,
                "Amount": order.get_order_total_price(),
                "Description": 'پرداخت از طریق درگاه زرین پال انجام شد',
                "CallbackURL": CallbackURL,
                "Metadata": {"mobile":user.mobile_number,"email":user.email},
            }
            req_headers = {'accept': 'application/json', 'content-type': 'application/json'}
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_headers)
            authority = req.json()['data']['authority']
            if len (req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code:{e_code},Error message:{e_message}")

        except ObjectDoesNotExist:
            return redirect('orders:checkout_order', order_id)

