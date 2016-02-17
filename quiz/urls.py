from django.conf.urls import url
from . import views

app_name = "quiz"
urlpatterns = [
    url(r'enviardata$', views.enviardata, name='enviardata'),
    url(r'$', views.quizindex, name='quizindex'),
]
