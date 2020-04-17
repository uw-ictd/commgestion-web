from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from web import public_view
from web.forms import UserSearchTimeForm

from . import network_stats_view
from . import network_users_view
from . import profiles_view


def public_info(request):
    gauge = public_view.generate_test_data()
    return render(request, 'public_info.html', context=gauge)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def network_stats(request):
    context = network_stats_view.generate_test_data()
    return render(request, 'network_stats.html', context=context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def profiles(request):
    subs = profiles_view.generate_table()
    return render(request, 'profiles.html', context=subs)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def network_users(request):
    if request.method == 'POST':
        form = UserSearchTimeForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            context = network_users_view.generate_test_data(from_date=from_date, to_date=to_date)
            print(context)
        else:
            context = network_users_view.generate_test_data()
    else:
        context = network_users_view.generate_test_data()
    context['form'] = UserSearchTimeForm()
    return render(request, 'network_users.html', context=context)
