from django.shortcuts import render

from web import public_view
from . import stats_view
from . import usuario_view


# Create your views here.
def home(request):
    return render(request, 'home.html')


def net_stats(request):
    context = stats_view.generate_test_data()
    return render(request, 'stats.html', context=context)


def public_info(request):
    gauge = public_view.generate_test_data()
    print(gauge)
    return render(request, 'public_info.html', context=gauge)


def profile(request):
    return render(request, 'profile.html')


def usuario(request):
    context = usuario_view.generate_test_data()
    return render(request, 'usuario_pie.html', context=context)