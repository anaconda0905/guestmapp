# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .forms import LoginForm, SignUpForm

from users.models import User
from order.models import Order
from scan.models import ScanTable, ScanDetailsTable

import json
import datetime


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_staff and user.is_active:
                    login(request, user)
                    return redirect("/administration")
                else:
                    msg = "You are authenticated as "+user.username+", but are not authorized to access this page.Would you " \
                          "like to login to a different account?"
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            print(form)
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


@user_passes_test(lambda u:u.is_staff, login_url="/administration/login/")
def index(request):
    cur_month = datetime.datetime.now().month
    cur_year = datetime.datetime.now().year
    orders_month = []
    users = User.objects.all()
    orders = Order.objects.all()
    users_count = users.__len__()
    orders_count = orders.__len__()
    total_payout = 0.0
    cur_month_payout = 0.0
    pending_orders = 0
    ready_orders = 0
    working_orders = 0
    completed_orders = 0
    confirmed_orders = 0
    cancelled_orders = 0
    month_orders = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0,
        '7': 0,
        '8': 0,
        '9': 0,
        '10': 0,
        '11': 0,
        '12': 0,
    }

    # set next month None
    for i in range(cur_month + 1, 13):
        month_orders[str(i)] = None

    for order in orders:
        month_orders[str(order.created_at.month)] += 1
        if order.created_at.month == cur_month:
            cur_month_payout += order.price / 100
            if orders_month.__len__() <= 10:
                orders_month.append(order)

        total_payout += order.price / 100
        if order.status == 0:
            pending_orders += 1
        if order.status == 1:
            ready_orders += 1
        if order.status == 2:
            working_orders += 1
        if order.status == 3:
            completed_orders += 1
        if order.status == 4:
            confirmed_orders += 1
        if order.status == 5:
            cancelled_orders += 1

    return render(request, "index.html",
                  {
                      'users': users,
                      'users_count': users_count,
                      'orders': orders,
                      'orders_month': orders_month,
                      'orders_count': orders_count,
                      'total_payout': round(total_payout, 2),
                      'pending_orders': round(pending_orders / orders_count, 2) * 100,
                      'ready_orders': round(ready_orders / orders_count, 2) * 100,
                      'working_orders': round(working_orders / orders_count, 2) * 100,
                      'completed_orders': round(completed_orders / orders_count, 2) * 100,
                      'confirmed_orders': round(confirmed_orders / orders_count, 2) * 100,
                      'cancelled_orders': round(cancelled_orders / orders_count, 2) * 100,
                      'month_orders': json.dumps(month_orders),
                      'cur_month': cur_month,
                      'cur_year': cur_year,
                      'cur_month_payout': round(cur_month_payout, 2),
                  })


@login_required(login_url="/administration/login/")
def all_orders(request):
    orders = Order.objects.all()
    orders_count = orders.__len__()
    return render(request, "orders/orders.html",
                  {
                      'orders': orders,
                      'orders_count': orders_count,
                  })


def test(request):
    return render(request, "forms.html")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
