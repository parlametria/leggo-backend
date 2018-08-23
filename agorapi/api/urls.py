from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^proposicoes/?$', views.ProposicaoList.as_view()),
]
