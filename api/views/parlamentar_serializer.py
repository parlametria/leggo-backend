
from rest_framework import serializers, generics
from django.db.models import Sum, Count, OuterRef, Subquery
from django.core.paginator import Paginator

from api.model.ator import Atores
from api.model.autoria import Autoria
from api.model.interesse import Interesse


class ParlamentaresSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    id_leggo = serializers.IntegerField()
    nome_autor = serializers.CharField()
    partido = serializers.CharField()
    uf = serializers.CharField()
    casa = serializers.CharField()
    bancada = serializers.CharField()
    total_documentos = serializers.IntegerField()
    peso_documentos = serializers.IntegerField()
    n_autorias = serializers.IntegerField()


class ParlamentaresList(generics.ListAPIView):
    '''
    Dados de todos os parlamentares. Lista informações agregadas
    de parlamentares como nome, atividade no congresso, vezes que foi autor,
    relator ou presidente de comissão, etc.
    '''
    serializer_class = ParlamentaresSerializer

    def get_queryset(self):
        # Calcula quantidade de autorias de cada ator
        autorias = (Autoria.objects.filter(id_autor=OuterRef('id_autor'))
                                   .values('id_autor')
                                   .annotate(n_autorias=Count('id_autor')))

        # Seleciona ranking ou define ranking padrão
        ranking_arg = self.request.query_params.get('ranking')
        if ranking_arg == 'ativos-twitter':
            ranking = '-discursos_twitter'
        elif ranking_arg == 'papeis-importantes':
            ranking = '-n_autorias'
        elif ranking_arg == 'peso-politico':
            ranking = '-peso_politico'
        else:
            ranking = '-peso_documentos'

        # Junta todos os dados dos parlamentares e os ordena
        todos_atores = Atores.objects.values(
                'uf', 'partido', 'casa', 'bancada',
                'id_leggo', 'id_autor', 'nome_autor'
        ).annotate(
            total_documentos=Sum('num_documentos'),
            peso_documentos=Sum('peso_total_documentos'),
            n_autorias=Subquery(autorias.values('n_autorias'))
        ).order_by(ranking)

        # Retorna apenas os atores de um interesse específico
        interesse_arg = self.request.query_params.get('interesse')
        if interesse_arg is None:
            interesse_arg = 'leggo'
        interesses = Interesse.objects.filter(interesse=interesse_arg)
        atores_por_interesse = todos_atores.filter(id_leggo__in=interesses)

        # Implementa paginação
        paginador = Paginator(atores_por_interesse, 50)  # 50 parlamentares p/ página
        pagina = self.request.query_params.get('pagina')
        if pagina is None:
            pagina = 1
        elif int(pagina) > paginador.num_pages:
            pagina = paginador.num_pages
        else:
            pagina = int(pagina)

        # Retorna página com parlamentares
        return paginador.page(pagina)
