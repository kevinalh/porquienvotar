from django import forms

from .models import Opinion_RelPropuesta, PerfilUsuario, TokenUsuario
from django.utils.translation import ugettext_lazy as _


class RespuestaForm (forms.ModelForm):
    class Meta:
        model = Opinion_RelPropuesta
        fields = ('justificacion', 'fuente', 'valor_propuesta', 'paginadelplan', 'link_fuente')


class TokenForm (forms.Form):
    token_input = forms.UUIDField(label='token_input')

    def clean(self):
        cleaned_data = super(TokenForm, self).clean()
        token_input = cleaned_data.get("token_input")
        if token_input:
            try:
                obj_token = TokenUsuario.objects.get(inv_token=token_input)
            except obj_token.DoesNotExist:
                # No existe el token en la lista de tokens posibles
                raise forms.ValidationError(_('El token no existe'), code='invalid')
            else:
                if PerfilUsuario.objects.filter(token=obj_token).exists():
                    # El token existe pero ya esta siendo usado
                    raise forms.ValidationError(_('El token ya ha sido usado'), code='invalid')
