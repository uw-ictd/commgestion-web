from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from web import public_view
from web.forms import UserSearchTimeForm
from . import stats_view
from . import usuario_view
from . import profile_view


# Create your views here.
@login_required
@user_passes_test(lambda u: u.is_superuser)
def net_stats(request):
    context = stats_view.generate_test_data()
    return render(request, 'stats.html', context=context)


def public_info(request):
    gauge = public_view.generate_test_data()
    # TODO: Check if you want to re-render this as a new request or use `redirect()` built in django
    return render(request, 'public_info.html', context=gauge)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def profile(request):
    subs = profile_view.generate_table()
    return render(request, 'profile.html', context=subs)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def usuario(request):
    if request.method == 'POST':
        form = UserSearchTimeForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            context = usuario_view.generate_test_data(from_date=from_date, to_date=to_date)
        else:
            context = usuario_view.generate_test_data()
    else:
        context = usuario_view.generate_test_data()
    context['form'] = UserSearchTimeForm()
    return render(request, 'usuario_pie.html', context=context)
