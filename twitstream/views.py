from django.shortcuts import render


def twitter_candidatos(request):
    context = []
    return render(request, 'twitstream/twit_index.html', context)
