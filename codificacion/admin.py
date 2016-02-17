from django.contrib import admin

from .models import TokenUsuario, PerfilUsuario

admin.site.register(TokenUsuario)
admin.site.register(PerfilUsuario)
