from django.db.models.signals import post_save
from django.dispatch import receiver

from quiz.models import Propuesta, Candidato, RelPropuestas


@receiver(post_save, sender=Propuesta)
def relaciona_propuestas(sender, instance, created, **kwargs):
    candidatos = Candidato.objects.all()
    for candidato in candidatos:
        RelPropuestas.objects.get_or_create(propuesta_relpropuestas=instance,
                                            candidato_relpropuestas=candidato, )
