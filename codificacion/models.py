# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

import uuid

from quiz.models import RelPropuestas

FUENTES_POSIBLES = (('Plan_de_Gobierno', 'Plan de Gobierno'),
                    ('Entrevista_TV', 'Entrevista (TV)'),
                    ('Entrevista_Escrita', 'Entrevista (Escrita)'),
                    ('Entrevista_Radio', 'Entrevista (Radio)'),
                    )


class TokenUsuario(models.Model):
    inv_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre_apellido = models.CharField(max_length=60, blank=True, default='')
    facebook = models.URLField(blank=True, null=True)

    def __str__(self):
        if self.nombre_apellido:
            return self.nombre_apellido
        else:
            return str(self.inv_token)

    class Meta:
        managed = True


class PerfilUsuario(models.Model):

    GENDER_CHOICES = (('Masculino', 'Masculino'),
                      ('Femenino', 'Femenino'),
                      ('Otros', 'Otros'),
                      ('', 'No especificar'),
                      )

    # Hay algunos problemas que ocurren si no se pone primary_key = True
    # Ver http://stackoverflow.com/questions/1910359/creating-a-extended-user-profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,
                                unique=True, related_name='perfil_usuario')
    gender = models.CharField(max_length=10, blank=True, default="", choices=GENDER_CHOICES, null=True)
    token = models.OneToOneField(TokenUsuario, on_delete=models.SET_NULL, null=True)

    def arroba(self):
        ''' Devuelve 'o', 'a' o arroba dependiendo del genero especificado por el usuario '''

        if self.gender == 'Masculino':
            return 'o'
        elif self.gender == 'Femenino':
            return 'a'
        else:
            return '@'

    def revisar_token(self):
        ''' Verifica que el usuario tiene un token. De ser el caso, devuelve True '''

        if self.token is None:
            return False
        else:
            return True

    def __str__(self):
        return self.user.username

    class Meta:
        managed = True


class Opinion_RelPropuesta(models.Model):

    VOTOS_PERMITIDOS = ((-1, 'En desacuerdo'),
                        (0, 'Neutral'),
                        (1, 'De acuerdo'), )

    user = models.ForeignKey(PerfilUsuario, on_delete=models.PROTECT)
    relpropuesta = models.ForeignKey(RelPropuestas, null=True, on_delete=models.SET_NULL)
    tiempo_subida = models.DateTimeField(auto_now_add=True, blank=True)

    # Necesarios
    justificacion = models.TextField("justificación", max_length=2000, blank=True)
    fuente = models.CharField(default='Plan_de_Gobierno', max_length=25, choices=FUENTES_POSIBLES)
    valor_propuesta = models.SmallIntegerField("posición", default=0, choices=VOTOS_PERMITIDOS)

    # Opcionales segun fuente
    paginadelplan = models.PositiveSmallIntegerField("página del Plan", default=0, blank=True)
    link_fuente = models.URLField("URL de la fuente", blank=True)

    def __str__(self):
        return ('Opinion de ' + self.user.username + 'sobre ' + self.relpropuesta.propuesta_relpropuestas +
                '-' + self.relpropuesta.candidato_relpropuestas)

    class Meta:
        managed = True
        unique_together = ("user", "relpropuesta")
