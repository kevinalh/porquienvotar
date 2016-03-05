from django.db import models
from quiz.models import Candidato


class DataTwitter(models.Model):
    """Guarda las menciones de cada candidato desde el reseteo hasta el momento en el campo tiempo"""
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    tiempo = models.DateTimeField()
    menciones = models.PositiveIntegerField(default=0)

    def fecha_y_hora(self):
        """Recorta el campo tiempo para que se pueda usar directamente en Google Charts"""
        return '%s/%s, %s:00' % (self.tiempo.day,
                                 self.tiempo.month,
                                 self.tiempo.hour,)

    def __str__(self):
        return '%s: %s' % (self.candidato.alias_candidato(),
                           self.tiempo)

    class Meta:
        unique_together = ("candidato", "tiempo")


class Tweet(models.Model):
    text = models.CharField(max_length=200)
    id_str = models.CharField(max_length=21, primary_key=True)
    user_id_str = models.CharField(max_length=21, blank=True, null=True)
    puntos = models.PositiveSmallIntegerField(default=0)
    tiempo = models.DateTimeField(auto_now_add=True)
    candidatos = models.ManyToManyField(Candidato, blank=True)

    def __str__(self):
        return self.id_str


class Keyword(models.Model):
    key = models.CharField(max_length=22, unique=True)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, blank=True, null=True)
    puntos = models.PositiveSmallIntegerField(default=1)
    para_filtro = models.BooleanField(default=True)
    hashtag = models.BooleanField(default=False)
    twitter_del_candidato = models.BooleanField(default=False)

    def __str__(self):
        if self.hashtag:
            return '#' + self.key
        else:
            return self.key
