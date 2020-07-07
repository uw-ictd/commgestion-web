import random

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from datetime import timedelta

import django.http
from django.utils import timezone
from django.db import transaction

from web.forms import (
    UserSearchTimeForm,
    AddSubscriberForm,
    EditSubscriberForm,
    DeleteSubscriberForm,
)
from web.models import Subscriber

from . import (_api, _network_stats, _network_users, _profiles, _public)


# Redefine api as a publicly exportable top level object in the package.
api = _api

def public_info(request):
    return render(request,
                  'public_info.html',
                  context=_public.generate_context(),
                  )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def network_stats(request):
    context = _network_stats.generate_test_data()
    return render(request, 'network_stats.html', context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def profiles(request):
    context = _profiles.generate_table()
    context['add_form'] = AddSubscriberForm()
    context['edit_form'] = EditSubscriberForm()
    context['del_form'] = DeleteSubscriberForm()
    if request.method == 'POST':
        form = AddSubscriberForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                User.objects.create(
                    username=form.cleaned_data['imsi'],
                    email=form.cleaned_data['email'],
                    password="temp",
                )
                user = User.objects.get(username=form.cleaned_data['imsi'])
                roleNum = roleConversion(form.cleaned_data['role'])
                statusNum = connectionConversion(form.cleaned_data['connection_status'])

                Subscriber.objects.create(
                    user=user,
                    phonenumber=form.cleaned_data['phone'],
                    display_name=form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'],
                    imsi=form.cleaned_data['imsi'],
                    guti="guti_value" + str(random.randint(0, 100)),
                    is_local=True, #how do we determine local or not local
                    role=roleNum,
                    connectivity_status=statusNum,
                    last_time_online=timezone.now(),
                    rate_limit_kbps=form.cleaned_data['rate_limit'],
                )
        else:
            context['add_form'] = form
            print(form.errors)
            print('invalid')

    return render(request, 'profiles.html', context=context)

def roleConversion(roleString):
    if roleString == 'Admin':
        return 1
    if roleString == 'User':
        return 2

def connectionConversion(connection):
    if connection == 'Online':
        return 1
    if connection == 'Offline':
        return 2
    if connection == 'Blocked':
        return 3

@login_required
@user_passes_test(lambda u: u.is_superuser)
def network_users(request):
    if request.method == 'POST':
        form = UserSearchTimeForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
    else:
        from_date = datetime.now() - timedelta(days=7)
        to_date = datetime.now()
    context = _network_users.generate_context(from_date=from_date, to_date=to_date)
    context['form'] = UserSearchTimeForm()
    return render(request, 'network_users.html', context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_form(request):
    if request.method == 'POST':
        form = AddSubscriberForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            imsi = form.cleaned_data['imsi']
            # guti = form.cleaned_data['guti']
            # phone = form.cleaned_data['phone']
            # resident_status = form.cleaned_data['resident_status']
            role = form.cleaned_data['role']
            rate_limit = form.cleaned_data['rate_limit']
            connection_status = form.cleaned_data['connection_status']
            context = network_users.lookup_user(imsi)
        else:
            print(form.errors)
    return render(request, 'add_form.html', context=AddSubscriberForm())

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_form(request):
    return render(request, 'edit_form.html', context=EditSubscriberForm())

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_form(request):
    return render(request, 'delete_form.html', context=DeleteSubscriberForm())