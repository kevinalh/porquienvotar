from django.conf.urls import url
from . import views


app_name = "codificacion"
urlpatterns = [
    url(r'^(?P<propuesta_id>[0-9]+)/(?P<candidato_id>[0-9]+)$', views.CandProp, name='candprop'),
    url(r'^(?P<propuesta_id>[0-9]+)$', views.PropuestaDetalle, name='propdetalle'),
    url(r'$', views.CodeIndex, name='codeindex'),
]
