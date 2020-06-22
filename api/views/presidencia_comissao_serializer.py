from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import json
import requests

from api.model.ator import Atores
from api.utils.filters import get_filtered_interesses
from api.utils.presidencia_comissao import(
    get_comissao_parlamentar
)

class PresidenciaComissaoSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_comissao = serializers.IntegerField()
    id_autor_voz = serializers.IntegerField()
    quantidade_comissao_presidente = serializers.IntegerField()
    info_comissao = serializers.CharField()


class PresidenciaComissaoLista(generics.ListAPIView):
   
    serializer_class = PresidenciaComissaoSerializer

    def get_queryset(self):
        '''
        Retorna informações sobre os parlamentares presidentes de comissões. 
        '''
       
        data = get_comissao_parlamentar()
        
        return data


