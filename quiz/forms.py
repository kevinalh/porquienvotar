from django.forms import ModelForm

from .models import Respuesta


class RespuestaForm (ModelForm):
    class Meta:
        model = Respuesta
        fields = ['respuesta']
