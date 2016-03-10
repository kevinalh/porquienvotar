from django.shortcuts import render, get_list_or_404
from django.utils.timezone import make_aware, utc
from django.db.models import Max

from quiz.models import Candidato
from .models import Tweet

import json
from datetime import datetime, timedelta
import pytz

# import pdb


def twitter_candidatos(request):
    lista_candidatos = get_list_or_404(Candidato, entra_candidato=True)
    tiempo_inicio = make_aware(datetime(2016, 3, 8, 0, 0, 0), utc)
    diferencia_tiempo = timedelta(hours=1)
    tiempo_final = Tweet.objects.filter(analizado=True).aggregate(Max('created_at'))['created_at__max']
    final_range = tiempo_final - tiempo_inicio
    pedazos = int(final_range / diferencia_tiempo)
    lista_tiempos = [tiempo_inicio + x*diferencia_tiempo for x in range(1, pedazos)]
    diccionario = {}
    tweets = Tweet.objects.filter(analizado=True)
    for tiempo in lista_tiempos:
        en_rango = tweets.filter(created_at__range=(tiempo - diferencia_tiempo, tiempo))
        dic_candidatos = {}
        for candidato in lista_candidatos:
            menciones = en_rango.filter(candidatos=candidato.id).count()
            dic_candidatos[candidato.alias_candidato] = menciones
        # pdb.set_trace()
        localizado = tiempo.astimezone(pytz.timezone('America/Lima'))
        diccionario[localizado.strftime("%Y,%m,%d,%H")] = dic_candidatos
    # pdb.set_trace()
    dic_json = json.dumps(diccionario, ensure_ascii=False)
    candidatos = json.dumps(list(dic_candidatos.keys()), ensure_ascii=False)
    tiempos = json.dumps([tiempo.astimezone(pytz.timezone('America/Lima')).strftime("%Y,%m,%d,%H")
                          for tiempo in lista_tiempos])
    context = {'datatwitter': dic_json,
               'candidatos': candidatos,
               'tiempos': tiempos}
    return render(request, 'twitstream/twit_index.html', context)
