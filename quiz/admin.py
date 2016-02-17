from django.contrib import admin

from .models import (Propuesta, Partido, Candidato, RelPropuestas, CategoriaPropuesta,
                     Visitante, Respuesta, IntentoVisitante)

admin.site.register(Propuesta)
admin.site.register(Partido)
admin.site.register(Candidato)
admin.site.register(RelPropuestas)
admin.site.register(CategoriaPropuesta)
admin.site.register(Visitante)
admin.site.register(IntentoVisitante)
admin.site.register(Respuesta)
