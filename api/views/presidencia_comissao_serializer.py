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
    idParlamentarVoz = serializers.IntegerField()
    idComissaoPresidencia = serializers.IntegerField()
    quantidadePresidenciaComissoes = serializers.IntegerField()
    infoComissao = serializers.CharField()


URL_PRESIDENCIA_COMISSAO = "https://perfil.parlametria.org/api/busca-parlamentar"

class PresidenciaComissaoLista(generics.ListAPIView):
   
    serializer_class = PresidenciaComissaoSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "interesse",
                openapi.IN_PATH,
                "Interesse para retornar peso político dos atores",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )

    def get_queryset(self):
       
        data = get_comissao_parlamentar()
        
        return data


