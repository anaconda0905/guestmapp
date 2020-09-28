from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from price.models import Price
from users.serializers import LoginSerializer, SignUpSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from users.backends import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from order.models import Order


class Login(ObtainAuthToken):
    serializer_class = LoginSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            print("valid")
            user = User.objects.get(email=serializer.validated_data['email'])
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'User is exist',
                    'success': True,
                    'errCode': -1,
                    'data': {
                        'id': user.id,
                        'full_name': user.username,
                        'email': user.email,
                        'isFirstUser': user.isFirstUser,
                        'token': token.key
                    }
                }, status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'User is not exist',
                    'errCode': 0,
                    'data': None
                })

        else:
            print(request.data)
            return Response({
                'success': False,
                'message': 'Faile to login',
                'errCode': 0,
                'data': None
            }, status.HTTP_200_OK)


class SignUp(APIView):
    serializer_class = SignUpSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data['email'])
            if user:
                return Response({
                    'success': False,
                    'message': 'Email is exist already',
                    'errCode': 0,
                    'data': None
                }, status.HTTP_200_OK)
            else:
                user = serializer.save_user(serializer.validated_data)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'success': True,
                    'message': 'Success to create user',
                    'errCode': -1,
                    'data': {
                        'id': user.id,
                        'full_name': user.username,
                        'isFirstUser': user.isFirstUser,
                        'email': user.email,
                        'token': token.key
                    }
                })

        else:
            return Response({
                'success': False,
                'message': 'Validation Error',
                'errCode': -1,
                'data': None
            }, status.HTTP_200_OK)


class Update(APIView):
    serializer_class = SignUpSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not request.user:
                return Response({
                    'success': False,
                    'message': 'User is not exist',
                    'errCode': 0,
                    'data': None
                }, status.HTTP_200_OK)
            else:
                user = request.user
                user.username = serializer.validated_data['full_name']
                user.email = serializer.validated_data['email']
                user.set_password(serializer.validated_data['password'])
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'success': True,
                    'message': 'Success to update user',
                    'errCode': -1,
                    'data': {
                        'id': user.id,
                        'full_name': user.username,
                        'isFirstUser': user.isFirstUser,
                        'email': user.email,
                        'token': token.key
                    }
                })

        else:
            return Response({
                'success': False,
                'message': 'Validation Error',
                'errCode': -1,
                'data': None
            }, status.HTTP_200_OK)


def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user, backend='users.backends.EmailOrUsernameModelBackend')
                    try:
                        order = Order.objects.filter(user=request.user)
                    except Order.DoesNotExist:
                        order = None

                    if order is not None:
                        exist_order = True
                    else:
                        exist_order = False

                    data = {'success': True, 'order': exist_order}
                else:
                    data = {'success': False, 'message': 'User is not active'}
            else:
                data = {'success': False, 'message': 'Invalid username or password'}

    return JsonResponse(data)


def ajax_register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                data = {'success': False, 'message': 'User already exists.'}
            else:
                try:
                    User.objects.create_user(username, email, password)
                    user = authenticate(username=username, password=password)
                    auth_login(request, user)

                except:
                    data = {'success': False, 'message': 'Unexpected error occured.'}

                data = {'success': True, 'message': 'User create successfully'}

    return JsonResponse(data)


def ajax_logout(request):
    logout(request)

    return redirect('home')


def home(request):
    order = None
    prices = Price.objects.all()
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(user=request.user)
        except Order.DoesNotExist:
            order = None
    return render(request, 'home.html', {'order': order, 'prices': prices})


@login_required
def guestmapp(request):
    orders = Order.objects.filter(user=request.user)
    order_exist = False
    if orders.__len__():
        order_exist = True

    order_completed = False
    orders_completed = Order.objects.filter(user=request.user, status=3)
    if orders_completed:
        order_completed = True

    order_progress = False
    for order in orders:
        if order.status == 0 or order.status == 1:
            if order.getImageUrl != "":
                order_progress = True
                break

    return render(request, 'guestmapp.html', {'orders': orders, 'order_exist': order_exist, \
                                              'order_completed': order_completed, 'order_progress': order_progress,
                                              'user': request.user})


@login_required
def planprices(request):
    orders = Order.objects.filter(user=request.user)
    prices = Price.objects.all()
    firstUser = 0
    if request.user.isFirstUser:
        firstUser = 1

    order_exist = False
    if orders.__len__():
        order_exist = True
    return render(request, 'planprices.html',
                  {'order_exist': order_exist, 'prices': prices, 'isFirstUser': firstUser})


@login_required
def ownguestmapp(request):
    orders = Order.objects.filter(user=request.user).filter(Q(status=3) | Q(status=5))
    order_exist = False

    if orders.__len__():
        order_exist = True
    return render(request, 'ownguestmapp.html', {'orders': orders})


@login_required
def newpassword(request):
    return render(request, 'newpassword.html')
