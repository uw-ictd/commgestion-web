import random
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from web.forms import (
    UserSearchTimeForm,
    AddSubscriberForm,
    EditSubscriberForm,
    DeleteSubscriberForm,
)
from web.models import Subscriber

from . import _api, _network_stats, _network_users, _subscribers, _public


# Redefine api as a publicly exportable top level object in the package.
api = _api


def public_info(request):
    return render(
        request,
        "public_info.html",
        context=_public.generate_context(),
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def network_stats(request):
    context = _network_stats.generate_test_data()
    return render(request, "network_stats.html", context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def subscribers(
    request,
    status=None,
    add_form_state=AddSubscriberForm(),
    edit_form_state=EditSubscriberForm(),
    del_form_state=DeleteSubscriberForm(),
    active_form=None,
):
    context = _subscribers.generate_table()
    context["add_form"] = add_form_state
    context["edit_form"] = edit_form_state
    context["del_form"] = del_form_state
    context["status"] = status
    context["active_form"] = active_form
    return render(request, "subscribers.html", context=context)


def roleConversion(roleString):
    if roleString == "Admin":
        return 1
    if roleString == "User":
        return 2


def connectionConversion(connection):
    if connection == "Authorized":
        return 1
    if connection == "Blocked":
        return 2


@login_required
@user_passes_test(lambda u: u.is_superuser)
def network_users(request):
    if request.method == "POST":
        form = UserSearchTimeForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
    else:
        from_date = datetime.now() - timedelta(days=7)
        to_date = datetime.now()
    context = _network_users.generate_context(from_date=from_date, to_date=to_date)
    context["form"] = UserSearchTimeForm()
    return render(request, "network_users.html", context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_form(request):
    if request.method == "POST":
        form = AddSubscriberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["imsi"]
            with transaction.atomic():
                User.objects.create(
                    username=username,
                    email="",
                    password="temp",
                )
                user = User.objects.get(username=form.cleaned_data["imsi"])
                roleNum = Subscriber.Role.USER_ROLE
                statusNum = connectionConversion(
                    form.cleaned_data["authorization_status"]
                )

                Subscriber.objects.create(
                    user=user,
                    msisdn=form.cleaned_data["msisdn"],
                    display_name=form.cleaned_data["name"],
                    imsi=form.cleaned_data["imsi"],
                    is_local=True,  # how do we determine local or not local
                    role=roleNum,
                    authorization_status=statusNum,
                    last_time_online=timezone.now(),
                    rate_limit_kbps=form.cleaned_data["rate_limit"],
                    equipment="unknown",
                    created=timezone.now(),
                    subscription_date=timezone.now(),
                    subscription_status=Subscriber.SubscriptionStatusKinds.PAID,
                )

            return subscribers(
                request,
                status={
                    "outcome": "success",
                    "message": "Successfully added user {}".format(username),
                },
            )
        else:
            return subscribers(
                request,
                add_form_state=form,
                active_form="ModalAddForm",
            )

    else:
        return redirect("subscribers")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_form(request):
    if request.method == "POST":
        form = EditSubscriberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["imsi"]
            with transaction.atomic():
                prev_user = User.objects.get(username=username)
                prev_subscriber = Subscriber.objects.get(user=prev_user)
                prev_subscriber.msisdn = form.cleaned_data["msisdn"]
                prev_subscriber.display_name = form.cleaned_data["name"]
                prev_subscriber.imsi = form.cleaned_data["imsi"]
                prev_subscriber.authorization_status = connectionConversion(
                    form.cleaned_data["authorization_status"]
                )
                prev_subscriber.rate_limit_kbps = form.cleaned_data["rate_limit"]
                prev_subscriber.last_time_online = timezone.now()
                prev_subscriber.save()
            return subscribers(
                request,
                status={
                    "outcome": "success",
                    "message": "Successfully edited user {}".format(username),
                },
            )
        else:
            return subscribers(
                request,
                edit_form_state=form,
                active_form="ModalEditForm",
            )
    else:
        return redirect("subscribers")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_form(request):
    if request.method == "POST":
        form = DeleteSubscriberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["imsi"]
            with transaction.atomic():
                prev_user = User.objects.get(username=username)
                Subscriber.objects.filter(user=prev_user).delete()
                User.objects.filter(username=username).delete()
            return subscribers(
                request,
                status={
                    "outcome": "success",
                    "message": "Successfully deleted user {}".format(username),
                },
            )
        else:
            return subscribers(
                request,
                del_form_state=form,
                active_form="ModalDeleteForm",
            )
    else:
        return redirect("subscribers")
