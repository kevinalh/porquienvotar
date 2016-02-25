"""porquienvoto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from homepage import views as homviews
from django.contrib.auth import views as auth_views
from codificacion.views import ConfigCuenta, RedirectCuenta, Registro

urlpatterns = [
    url(r'^preguntastriviales123/', include(admin.site.urls)),
    url(r'^quiz/', include('quiz.urls', namespace="quiz")),
    url(r'^codificacion/', include('codificacion.urls', namespace="codificacion")),
    url(r'^$', homviews.index_view, name="indice"),
    url(r'^registro/$', Registro, name='registro'),
    url(r'^login/', auth_views.login, {'template_name': 'cuentas/loginpage.html',
                                       'extra_context': {'next': '/codificacion'}},
        name='login'),
    url(r'^change_password/', auth_views.password_change,
        {'template_name': 'cuentas/change_password.html'}, name='change_password'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'cuentas/logoutpage.html'}, name='logout'),
    url(r'^cuenta/', ConfigCuenta, name='cuenta'),
    url(r'^accounts/profile/', RedirectCuenta),
    # FALTA:
    # url(r'^password_change/$', auth_views.password_change, name='password_change'),
    # url(r'^password_change/done/$', auth_views.password_change_done, name='password_change_done'),
    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
