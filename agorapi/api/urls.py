from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^proposicoes/?$', views.ProposicaoList.as_view()),
    url(r'^proposicoes/(?P<pk>[0-9]+)/?$', views.ProposicaoDetail.as_view()),
    url(r'^info/?$', views.Info.as_view()),
]
