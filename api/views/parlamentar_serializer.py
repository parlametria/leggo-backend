
from rest_framework import serializers, generics
from api.model.ator import Atores
from api.model.autoria import Autoria
from django.db.models import Sum, Count, OuterRef, Subquery, Case, When, IntegerField


# class DocumentosSerializer(serializers.Serializer):
#     tipo_generico = serializers.CharField()
#     num_documentos = serializers.IntegerField()
#     peso_total_documentos = serializers.FloatField()
      

class ParlamentaresSerializer(serializers.Serializer):
    id_autor = serializers.IntegerField()
    nome = serializers.CharField()
    partido = serializers.CharField()
    uf = serializers.CharField()
    casa = serializers.CharField()
    bancada = serializers.CharField()
    total_documentos = serializers.IntegerField()
    peso_documentos = serializers.IntegerField()
    n_autorias = serializers.IntegerField()

class ParlamentaresList(generics.ListAPIView):
    '''
    Dados de todos os parlamentares. Lista informações agregadas de parlamentares como nome, atividade no congresso, vezes que foi autor, relator ou presidente de comissão, etc.
    '''
    serializer_class = ParlamentaresSerializer

    def get_queryset(self):
        unicos = Atores.objects.filter(id_autor=OuterRef('id_autor')).distinct('id_autor')
        autorias = Autoria.objects.filter(id_autor=OuterRef('id_autor')).values('id_autor').annotate(n_autorias=Count('id_autor'))

        return Atores.objects.values('id_autor').annotate(
            total_documentos=Sum('num_documentos'),
            peso_documentos=Sum('peso_total_documentos'),
            nome=Subquery(unicos.values('nome_autor')[:1]),
            partido=Subquery(unicos.values('partido')[:1]),
            uf=Subquery(unicos.values('uf')[:1]),
            casa=Subquery(unicos.values('casa')[:1]),
            bancada=Subquery(unicos.values('bancada')[:1]),
            n_autorias=Subquery(autorias.values('n_autorias'))
        )