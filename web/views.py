from django.shortcuts import render
from . import stats_view


# Create your views here.
def home(request):
    return render(request, 'home.html')


def net_stats(request):
    context = stats_view.generate_test_data()
    return render(request, 'stats.html', context=context)


def public_info(request):
    return render(request, 'public_info.html')


def profile(request):
    return render(request, 'profile.html')


def usuario(request):
    return render(request, 'usuario_pie.html')
