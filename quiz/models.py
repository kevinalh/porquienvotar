# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.deletion import SET_NULL, CASCADE, SET_DEFAULT
from django.conf import settings

# from django.db.models.signals import post_save
# from .signals.handlers import relaciona_propuestas

from colorfield.fields import ColorField

VOTOS_PERMITIDOS = ((-1, 'En desacuerdo -'),
                    (0, 'Neutral'),
                    (1, 'De acuerdo'),)

IMPORTANCIAS_PERMITIDAS = ((0, '0'),
                           (1, '1'),
                           (2, '2'),
                           (3, '3'),
                           (4, '4'),)

SIN_CATEGORIZAR_ID = 99

# Estructural


class Partido (models.Model):
    nombre_partido = models.CharField(max_length=100, unique=True)
    web_partido = models.URLField(default='', blank=True)
    color_partido = ColorField(default='#FF0000')
    slug_partido = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.nombre_partido

    class Meta:
        managed = True


class Candidato (models.Model):
    nombre_candidato = models.CharField(max_length=40)
    segundonombre_candidato = models.CharField(max_length=40, blank=True)
    apellido_candidato = models.CharField(max_length=50, blank=True)
    segundoapellido_candidato = models.CharField(max_length=50, blank=True)
    alias_candidato = models.CharField(max_length=70, blank=True, default="", unique=True)

    entra_candidato = models.BooleanField(default=True)

    web_candidato = models.URLField(default="", blank=True)
    partido_candidato = models.OneToOneField(Partido, null=True, on_delete=CASCADE)

    slug_candidato = models.SlugField(blank=True, null=True, unique=True)
    voto_informado = models.URLField(default="", blank=True)

    def aliascandidato(self):
        if (self.alias_candidato == ""):
            return self.nombre_candidato + ' ' + self.apellido_candidato
        else:
            return self.alias_candidato

    def relacion_valores(self):
        propuestas_candidato = RelPropuestas.objects.filter(candidato_relpropuestas=self,
                                                            propuesta_relpropuestas__entra_propuesta=True, )
        tabla = {}
        for propuesta in propuestas_candidato:
            tabla[str(propuesta.propuesta_relpropuestas.id)] = str(propuesta.valor_propuesta)
            # tabla[propuesta.propuesta_relpropuestas.titulo_propuesta] = propuesta.valor_propuesta
        return tabla

    def __str__(self):
        return self.aliascandidato()

    class Meta:
        managed = True
        unique_together = ("nombre_candidato", "apellido_candidato")


class CategoriaPropuesta (models.Model):
    titulo_categoria = models.CharField(max_length=60)
    descripcion_categoria = models.CharField(max_length=1000)
    entra_categoria = models.BooleanField(default=True)
    color_categoria = ColorField(default='#FF0000')

    def __str__(self):
        return self.titulo_categoria

    class Meta:
        managed = True
        verbose_name = "categoria de Propuestas"
        verbose_name_plural = "categorias de Propuestas"
        ordering = ['-id']


class Propuesta (models.Model):
    titulo_propuesta = models.CharField(max_length=2000)
    entra_propuesta = models.BooleanField(default=False)
    descripcion_propuesta = models.CharField(max_length=2000)
    # La propuesta en formato adecuado para un cuestionario
    pregunta_propuesta = models.CharField(max_length=2000, default='?')
    categoria_propuesta = models.ForeignKey(CategoriaPropuesta, default=99, on_delete=SET_DEFAULT)

    def __str__(self):
        return self.titulo_propuesta

    class Meta:
        managed = True


class RelPropuestas (models.Model):
    propuesta_relpropuestas = models.ForeignKey(Propuesta, on_delete=CASCADE, default=1)
    candidato_relpropuestas = models.ForeignKey(Candidato, on_delete=CASCADE, default=1)
    justificacion = models.CharField(max_length=2000, default="", blank=True)
    paginadelplan = models.PositiveSmallIntegerField(default=0, blank=True)
    valor_propuesta = models.SmallIntegerField(default=None, null=True, blank=True, choices=VOTOS_PERMITIDOS)

    def __str__(self):
        return '%s : %s' % (self.candidato_relpropuestas.nombre_candidato,
                            self.propuesta_relpropuestas.titulo_propuesta)
        # return self.propuesta.titulo_propuesta

    class Meta:
        managed = True
        verbose_name = "relacion entre Propuesta y Candidato"
        verbose_name_plural = "relaciones entre Propuestas y Candidatos"
        unique_together = ("propuesta_relpropuestas", "candidato_relpropuestas")


# Contenido editado por el usuario


class Visitante (models.Model):
    ip_res = models.GenericIPAddressField(primary_key=True)
    sospechoso = models.BooleanField(default=False)
    baneado = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % str(self.ip_res)

    class Meta:
        managed = True


class IntentoVisitante (models.Model):
    visitante_intento = models.ForeignKey(Visitante, on_delete=CASCADE)
    intento_browser = models.PositiveSmallIntegerField(default=1)
    intento_db = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "%s" % str(self.visitante_intento.ip_res)

    class Meta:
        managed = True
        verbose_name = "intento de Visitante"
        verbose_name_plural = "intentos de Visitantes"
        unique_together = ("visitante_intento", "intento_db")


class Respuesta (models.Model):
    intento_res = models.ForeignKey(IntentoVisitante, on_delete=CASCADE)
    pregunta_res = models.ForeignKey(Propuesta, null=True, on_delete=SET_NULL)
    respuesta_res = models.SmallIntegerField(default=None, null=True, blank=True, choices=VOTOS_PERMITIDOS)
    importancia_res = models.SmallIntegerField(default=None, null=True, blank=True, choices=IMPORTANCIAS_PERMITIDAS)
    tiempo_res = models.DurationField(blank=True, null=True)

    def __str__(self):
        return "%s : %s : %s %s" % (str(self.intento_res.visitante_intento.ip_res), str(self.pregunta_res),
                                    str(self.intento_res.intento_db), str(self.intento_res.intento_browser))

    class Meta:
        managed = True
        unique_together = ("intento_res", "pregunta_res")
