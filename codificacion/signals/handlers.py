from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from codificacion.models import PerfilUsuario


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Para que esto funcione, ver apps.py
    if created:
        perfil_usuario = PerfilUsuario(user=instance)
        perfil_usuario.save()
