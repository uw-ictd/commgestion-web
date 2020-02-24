from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from web import public_view
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
    context = usuario_view.generate_test_data()
    return render(request, 'usuario_pie.html', context=context)
