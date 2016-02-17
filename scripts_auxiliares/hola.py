import random
from quiz.models import Candidato, Propuesta, RelPropuestas

for candidato in Candidato.objects.all():
    for propuesta in Propuesta.objects.all():
        hola, chau = RelPropuestas.objects.get_or_create(propuesta_relpropuestas=propuesta,
                                                         candidato_relpropuestas=candidato, )
        hola.valor_propuesta = random.randint(-1, 1)
        hola.save()
