from django.shortcuts import render, get_list_or_404

from .models import Propuesta, Candidato, Visitante, Respuesta, IntentoVisitante, CategoriaPropuesta

import json
import logging
from django.http.response import Http404, HttpResponse
from django.db.models import Max

from ipware.ip import get_real_ip, get_ip
# import pdb
from django.core.exceptions import ValidationError, MultipleObjectsReturned


def quizindex(request):
    # lista_propuestas = get_list_or_404(Propuesta, entra_propuesta=True)
    lista_candidatos = get_list_or_404(Candidato, entra_candidato=True)
    lista_categorias = get_list_or_404(CategoriaPropuesta, entra_categoria=True)
    diccionario = {}

    for candidato_bucle in lista_candidatos:
        diccionario[str(candidato_bucle.id)] = candidato_bucle.relacion_valores()
        # diccionario[str(candidato_bucle.aliascandidato())] = candidato_bucle.relacion_valores()
        # pdb.set_trace()

    relpropuestas = json.dumps(diccionario)

    propuestas = {}
    for categoria in lista_categorias:
        propuestas[categoria] = categoria.propuesta_set.exclude(entra_propuesta=False)

    context = {'propuestas': propuestas,
               # 'lista_propuestas': lista_propuestas,
               'lista_candidatos': lista_candidatos,
               'relpropuestas': relpropuestas, }
    return render(request, 'quiz/quizindex.html', context)


def enviardata(request):
    # DEPLOYMENT: Recordar cambiar get_ip a get_real_ip
    if request.method == 'POST':
        ip = get_real_ip(request)
        # ip = get_ip(request)
        logger = logging.getLogger(__name__)

        if ip is not None:
            try:
                invitado, creado = Visitante.objects.get_or_create(ip_res=ip)
            except MultipleObjectsReturned as e:
                logger.critical(e)
                return HttpResponse()

            if creado:
                database_tries = 0
            elif invitado.baneado is True:
                logger.info('Usuario baneado %s ha intentado entrar' % str(invitado.ip_res))
                return HttpResponse()
            else:
                agg_dbtries = IntentoVisitante.objects.filter(visitante_intento__ip_res=ip)
                if not agg_dbtries.exists():
                    database_tries = 0
                    logger.critical('Existe el Visitante pero no el IntentoVisitante para %s' % str(ip))
                else:
                    database_tries = agg_dbtries.aggregate(Max('intento_db'))['intento_db__max']

            intentoNAIVE = json.loads(request.POST.get('intento'))
            invitado_try = IntentoVisitante(visitante_intento=invitado,
                                            intento_browser=intentoNAIVE,
                                            intento_db=database_tries + 1, )
            try:
                invitado_try.full_clean()
            except ValidationError as e:
                invitado.sospechoso = True
                invitado.save()
                logger.warning(e)
                return HttpResponse()
            else:
                invitado_try.save()

            respuestas = json.loads(request.POST.get('respuestas_J'))
            importancias = json.loads(request.POST.get('importancias_J'))
            for pregunta_id in respuestas:
                respuesta_obj = Respuesta(intento_res=invitado_try,
                                          respuesta_res=respuestas[pregunta_id],
                                          pregunta_res=Propuesta.objects.get(pk=pregunta_id),
                                          importancia_res=importancias[pregunta_id], )
                try:
                    respuesta_obj.full_clean(validate_unique=True)
                except ValidationError as e:
                    invitado.sospechoso = True
                    invitado.save()
                    logger.warning(e)
                    return HttpResponse()
                else:
                    respuesta_obj.save()
            # pdb.set_trace()
            return HttpResponse('El ip actual es %s' % str(ip))
        else:
            return HttpResponse('El ip actual es %s' % str(ip))
    else:
        raise Http404('No se ha entrado correctamente')
