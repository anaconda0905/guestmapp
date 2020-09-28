from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from order.models import Order, Billing
from price.models import Price
from users.models import User
from scan.models import ScanTable
from order.serializers import OrderSerializer
from decouple import config
import stripe


class OrderViewSet(ModelViewSet):
    http_method_names = ['post', 'get']
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        orders = self.get_queryset()
        orderses = []
        for order in orders:
            query = order.to_dict()
            try:
                scans = ScanTable.objects.get(order=order.id)
                query.update({"scan": scans.to_dict()})
            except:
                query.update({"scan": {}})
            orderses.append(query)

        return JsonResponse({
            "success": True,
            "message": "success to get order list",
            "errCode": -1,
            "data": orderses
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.save(user=request.user)
        billing = Billing.objects.get(order=order)
        if int(request.data['productType']) < 0 or int(request.data['productType']) > 4:
            return JsonResponse({
                'success': False,
                'message': "Product Type is invalid",
                'errCode': -1,
                'data': None,
            })

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            customer = stripe.Customer.create(
                email=order.user.email,
                description="Customer",
            )
            billing_str = billing.expiry_date
            exp_date = billing_str.split("/")
            if exp_date.__len__() != 2:
                order.delete()
                return JsonResponse({
                    'success': False,
                    'message': 'Fail to create order cause dating input format is wrong. Expected format is XX/XX',
                    'errCode': -1,
                    'data': None,
                })
            token = stripe.Token.create(
                card={
                    "number": billing.card_number,
                    "exp_month": exp_date[0],
                    "exp_year": "20" + exp_date[1],
                    "cvc": str(billing.cvv),
                },
            )
            # 4000 0000 0000 0077 test card for payout
            # test
            # token = stripe.Token.create(
            #     card={
            #         "number": "4242424242424242",
            #         "exp_month": 8,
            #         "exp_year": 2021,
            #         "cvc": "314",
            #     },
            # )
            product_price = int(billing.price * 100)
            stripe.Customer.create_source(
                customer.id,
                source=token,
            )
            stripe.Charge.create(
                customer=customer.id,
                amount=product_price,
                currency='usd',
                description='description'
            )
            # 
            transfer = stripe.Transfer.create(
                amount=product_price,
                currency="usd",
                destination="acct_1HDMiwFlRRirkg6s",
                transfer_group=order.id,
            )
            billing.transaction_code = transfer.id
            billing.save()

            # user = get_object_or_404(User, pk = request.user.id)
            user = request.user
            user.isFirstUser = False
            user.save()

        except stripe.error.StripeError as e:
            body = e.json_body
            err = body['error']
            order.delete()
            return JsonResponse({
                'success': False,
                'message': err['message'],
                'errCode': -1,
                'data': None,
            })

        return JsonResponse({
            "success": True,
            "message": "success to create new order",
            "errCode": -1,
            "data": order.to_dict(),
        }, status=status.HTTP_200_OK)


class OrderCommit(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        order_id = self.request.data['order_id']
        status = self.request.data['status']
        order = get_object_or_404(Order, pk=order_id)
        order.status = status
        order.save()
        return JsonResponse({
            'success': True,
            'message': 'success to update order status',
            'errCode': -1,
            'data': None
        })


@login_required
def payout(request):
    if request.method == 'POST':
        productType = request.POST.get('productType', '').strip()
        metadata = request.POST.get('metadata', '').strip()
        tires = request.POST.get('tires', '').strip()
        price = request.POST.get('price', '').strip()
        card_name = request.POST.get('card_name', '').strip()
        card_number = request.POST.get('card_number', '').strip()
        cvv = request.POST.get('cvv', '').strip()
        expiry_date = request.POST.get('expiry_date', '').strip()

        product_price = int(float(price) * 100)

        order = Order()
        order.user = request.user
        order.product_type = productType
        order.metadata = metadata
        order.tires = tires
        order.price = product_price
        order.status = 0
        order.save()

        billing = Billing()
        billing.order = order
        billing.price = product_price
        billing.card_name = card_name
        billing.card_number = card_number
        billing.cvv = cvv
        billing.expiry_date = expiry_date
        billing.save()

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            customer = stripe.Customer.create(
                email=order.user.email,
                description="Customer",
            )
            billing_str = billing.expiry_date
            exp_date = billing_str.split("/")
            if exp_date.__len__() != 2:
                order.delete()
                return JsonResponse({
                    'success': False,
                    'message': 'Fail to create order cause dating input format is wrong. Expected format is XX/XX',
                    'errCode': -1,
                    'data': None,
                })
            token = stripe.Token.create(
                card={
                    "number": billing.card_number,
                    "exp_month": exp_date[0],
                    "exp_year": "20" + exp_date[1],
                    "cvc": str(billing.cvv),
                },
            )

            stripe.Customer.create_source(
                customer.id,
                source=token,
            )
            stripe.Charge.create(
                customer=customer.id,
                amount=product_price,
                currency='usd',
                description='description'
            )

            transfer = stripe.Transfer.create(
                amount=product_price,
                currency="usd",
                destination="acct_1HDMiwFlRRirkg6s",
                transfer_group=order.id,
            )
            billing.transaction_code = transfer.id
            billing.save()

            user = request.user
            user.isFirstUser = False
            user.save()

        except stripe.error.StripeError as e:
            body = e.json_body

            err = body['error']
            order.delete()
            return JsonResponse({
                'success': False,
                'message': err['message'],
                'errCode': -1,
                'data': None,
            })

        return JsonResponse({
            "success": True,
            "message": "success to create new order",
            "errCode": -1,
            "data": order.to_dict(),
        }, status=status.HTTP_200_OK)

    return JsonResponse({
        'success': False,
        'message': 'Fail to create order',
        'errCode': -1,
        'data': None,
    })
