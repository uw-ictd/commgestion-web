from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from datetime import timedelta

from web import public_view
from web.forms import UserSearchTimeForm, ModalForm, ModalEditForm

from . import network_stats_view
from . import network_users_view
from . import profiles_view


def public_info(request):
    return render(request,
                  'public_info.html',
                  context=public_view.generate_context(),
                  )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def network_stats(request):
    context = network_stats_view.generate_test_data()
    return render(request, 'network_stats.html', context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def profiles(request):
    context = profiles_view.generate_table()
    context['form'] = ModalForm()
    if request.method == 'POST':
        form = ModalForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            # phone = form.cleaned_data['phone']
            # imsi = form.cleaned_data['imsi']
            # guti = form.cleaned_data['guti']
            # resident_status = form.cleaned_data['resident_status']
            # role = form.cleaned_data['role']
            # connection_status = form.cleaned_data['connection_status']
            # password = form.cleaned_data['password']
            # print(first_name, last_name, email, phone, imsi, guti, resident_status, role, connection_status)
        else:
            context['form'] = form
            print(form.errors)
            print('invalid')
    return render(request, 'profiles.html', context=context)


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
    context = network_users_view.generate_context(from_date=from_date, to_date=to_date)
    context['form'] = UserSearchTimeForm()
    return render(request, 'network_users.html', context=context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addForm(request):
    if request.method == 'POST':
        form = ModalForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            imsi = form.cleaned_data['imsi']
            guti = form.cleaned_data['guti']
            phone = form.cleaned_data['phone']
            resident_status = form.cleaned_data['resident_status']
            role = form.cleaned_data['role']
            connection_status = form.cleaned_data['connection_status']
            context = network_users_view.lookup_user(imsi)
