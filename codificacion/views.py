# -*- encoding: utf-8 -*-

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from quiz.models import CategoriaPropuesta, Propuesta, Candidato, RelPropuestas

from .forms import RespuestaForm, TokenForm
from .models import TokenUsuario, Opinion_RelPropuesta
from django.shortcuts import redirect

# import pdb
import itertools

# Tests


def token_check(user):
    return user.perfil_usuario.revisar_token()

# Views


@login_required
def CodeIndex(request):
    usuario = request.user
    tokendescription = ("Es el código que se da previamente a los usuarios que han sido" +
                        " seleccionados para participar en el proyecto, que aún es cerrado")
    categorias = get_list_or_404(CategoriaPropuesta)
    propuestas = {}
    progresos = {}
    # numcandidatos = Candidato.objects.count()
    for categoria in categorias:
        propuestas[categoria] = categoria.propuesta_set.all()
    token_correcto = usuario.perfil_usuario.revisar_token()

    for propuesta in list(itertools.chain.from_iterable(propuestas.values())):
        progresos[propuesta] = Opinion_RelPropuesta.objects.filter(relpropuesta__propuesta_relpropuestas=propuesta) \
                                .count()

    # pdb.set_trace()

    context = {'arroba': usuario.perfil_usuario.arroba(),
               'genero': usuario.perfil_usuario.gender,
               'tokendesc': tokendescription,
               'propuestas': propuestas,
               # 'categorias': categorias,
               # 'numcandidatos': numcandidatos,
               'token_falta': not token_correcto,
               'progresos': progresos, }

    if request.method == 'POST' and not token_correcto:
        tokenform = context['formulario'] = TokenForm(request.POST)
        if tokenform.is_valid():
            usuario.perfil_usuario.token = TokenUsuario.objects.get(inv_token=request.POST['token_input'])
            usuario.perfil_usuario.save()
            if usuario.perfil_usuario.revisar_token():
                usuario.user_permissions.add()
            return redirect('codificacion:codeindex')
    elif not token_correcto:
        tokenform = context['formulario'] = TokenForm()
    else:
        tokenform = None

    return render(request, 'codificacion/codeindex.html', context)


@login_required
def ConfigCuenta(request):
    usuario = request.user
    try:
        aportes = Opinion_RelPropuesta.objects.filter(user=usuario.perfil_usuario).order_by('-tiempo_subida')[:10]
    except ObjectDoesNotExist:
        aportes = False
    context = {'usuario': usuario,
               'aportes': aportes}
    return render(request, 'codificacion/configcuenta.html', context)


@login_required
def PropuestaDetalle(request, propuesta_id):
    usuario = request.user
    propuesta = get_object_or_404(Propuesta, pk=propuesta_id)
    lista_candidatos = get_list_or_404(Candidato)
    relpropuestas = {}
    token_correcto = usuario.perfil_usuario.revisar_token()
    for candidato in lista_candidatos:
        relpropuestas[candidato] = RelPropuestas.objects.get(candidato_relpropuestas=candidato,
                                                             propuesta_relpropuestas=propuesta)
    context = {'usuario': usuario,
               'propuesta': propuesta,
               'relpropuestas': relpropuestas,
               'token_correcto': token_correcto, }
    return render(request, 'codificacion/propdetalle.html', context)


@user_passes_test(token_check)
@login_required
def CandProp(request, propuesta_id, candidato_id):
    usuario = request.user
    propuesta = get_object_or_404(Propuesta, pk=propuesta_id)
    candidato = get_object_or_404(Candidato, pk=candidato_id)
    relpropuesta_tmp = get_object_or_404(RelPropuestas,
                                         candidato_relpropuestas=candidato,
                                         propuesta_relpropuestas=propuesta, )
    if request.method == "POST":
        formulario = RespuestaForm(request.POST)
        if formulario.is_valid():
            post = formulario.save(commit=False)
            post.user = usuario
            post.relpropuesta = relpropuesta_tmp
            post.save()
            return redirect('propdetalle', propuesta_id=propuesta_id)
    elif Opinion_RelPropuesta.objects.filter(user=usuario.perfil_usuario, relpropuesta=relpropuesta_tmp).exists():
        opinion = Opinion_RelPropuesta.objects.get(user=usuario.perfil_usuario, relpropuesta=relpropuesta_tmp)
        data = {'justificacion': opinion.justificacion,
                'fuente': opinion.fuente,
                'valor_propuesta': opinion.valor_propuesta,
                'paginadelplan': opinion.paginadelplan,
                'link_fuente': opinion.link_fuente, }
        formulario = RespuestaForm(data)
    else:
        formulario = RespuestaForm()
    pdf_path = candidato.plan_de_gobierno
    context = {'usuario': usuario,
               'propuesta': propuesta,
               'candidato': candidato,
               'form': formulario,
               'pdf_path': pdf_path, }
    return render(request, 'codificacion/candprop.html', context)

# @login_required
# def EnviarData(request):
#     usuario = request.user


def RedirectCuenta(request):
    return redirect('cuenta')


def LoginPage(request):
    return render(request, 'codificacion/loginpage.html')
