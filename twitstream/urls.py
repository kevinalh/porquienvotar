from django.conf.urls import url

from . import views

app_name = "twitstream"
urlpatterns = [
    url(r'$', views.twitter_candidatos, name='twit'),
]
