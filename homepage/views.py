from django.shortcuts import render


def index_view(request):
    return render(request, 'homepage/indice.html')


def acerca_de(request):
    return render(request, 'homepage/acercade.html')
