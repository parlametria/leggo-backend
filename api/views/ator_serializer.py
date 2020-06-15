from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Prefetch, Sum

from api.model.ator import Atores
from api.model.etapa_proposicao import EtapaProposicao
from api.utils.filters import get_filtered_autores, get_filtered_interesses


class AtoresSerializerComissoes(serializers.ModelSerializer):
    class Meta:
        model = Atores
        fields = (
            'id_autor', 'nome_autor', 'partido', 'uf',
            'peso_total_documentos', 'num_documentos', 'tipo_generico',
            'sigla_local_formatada', 'is_important', 'nome_partido_uf'
        )


class AtoresProposicaoList(generics.ListAPIView):
    '''
    Dados de atores de uma proposição. Lista parlamentares que atuaram numa proposição
    com informações como o número de documentos criados e o peso do autor com relação
    aos documentos apresentados. A participação do parlamentar em um documento é
    inversamente proporcional à quantidade de parlamentares que assinaram o documento
    juntos: um documento feito por dois parlamentares terá valor de
    participação igual a 1/2 = 0.5. Desta forma o peso do ator é a soma das
    participações do parlamentar nos documentos relacionados à proposição.
    '''

    serializer_class = AtoresSerializerComissoes

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id_leggo', openapi.IN_PATH, 'id da proposição no sistema Leggo',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna os atores por proposição
        '''
        prop_leggo_id = self.kwargs['id_leggo']
        queryset = Atores.objects.filter(id_leggo=prop_leggo_id)
        return get_filtered_autores(self.request, queryset)


class AtoresAgregadosSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    nome_autor = serializers.CharField()
    partido = serializers.CharField()
    uf = serializers.CharField()
    casa = serializers.CharField()
    bancada = serializers.CharField()
    total_documentos = serializers.IntegerField()
    peso_documentos = serializers.IntegerField()


class AtoresAgregadosList(generics.ListAPIView):
    '''
    Informação agregada sobre parlamentares.
    '''
    serializer_class = AtoresAgregadosSerializer

    def get_queryset(self):
        '''
        Retorna dados básicos e de atividade parlamentar por interesse.
        '''
        interesse_arg = self.request.query_params.get('interesse')
        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = get_filtered_interesses(interesse_arg)

        atores = (
            Atores.objects
            .filter(id_leggo__in=interesses)
            .values('id_autor', 'nome_autor', 'uf', 'partido', 'casa', 'bancada')
            .annotate(
                total_documentos=Sum('num_documentos'),
                peso_documentos=Sum('peso_total_documentos')
            )
            .prefetch_related(Prefetch("interesse", queryset=interesses))
        )
        return atores

class AtoresRelatoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atores
        fields = (
            'nome_autor'
        )

class AtoresRelatoresList(generics.ListAPIView):

    serializer_class = AtoresRelatoresSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'interesse', openapi.IN_PATH, 'interesse da proposição no sistema Leggo',
                type=openapi.TYPE_STRING),
        ]
    )

    def get_queryset(self):
        '''
        Retorna os atores por proposição
        '''
        interesseArg = self.request.query_params.get("interesse")
        if interesseArg is None:
            interesseArg = 'leggo'
        interesses = get_filtered_interesses(interesseArg)
        print('interesses: ', interesses.values)
        queryset = Atores.objects.filter(id_leggo__in=interesses)
        print('queryset: ', queryset)
        atoresRelatores = []
        for etapa in EtapaProposicao.objects.all():
            quantRelatorias = 0
            if (etapa.relator_nome != 'Relator não encontrado'):
                for ator in Atores.objects.all():
                    if (ator.nome_autor in etapa.relator_nome):
                        quantRelatorias += 1

                atoresRelatores.append({
                    'nome_autor': etapa.relator_nome,
                    'relatorias': quantRelatorias
                })
        print('atores: ', atoresRelatores)

        return atoresRelatores