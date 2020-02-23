from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from web import public_view
from . import stats_view
from . import usuario_view
from . import profile_view


# Create your views here.

def net_stats(request):
    context = stats_view.generate_test_data()
    return render(request, 'stats.html', context=context)


def public_info(request):
    gauge = public_view.generate_test_data()
    # TODO: Check if you want to re-render this as a new request or use `redirect()` built in django
    return render(request, 'public_info.html', context=gauge)


def profile(request):
    subs = profile_view.generate_table()
    return render(request, 'profile.html', context=subs)


@login_required
def usuario(request):
    context = usuario_view.generate_test_data()
    return render(request, 'usuario_pie.html', context=context)