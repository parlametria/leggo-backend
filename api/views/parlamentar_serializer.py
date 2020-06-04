
from rest_framework import serializers, generics
from api.model.ator import Atores
from api.model.comissao import Comissao
from django.db.models import Sum, OuterRef, Subquery


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

class ParlamentaresList(generics.ListAPIView):
    '''
    Dados de todos os parlamentares. Lista informações agregadas de parlamentares como nome, atividade no congresso, vezes que foi autor, relator ou presidente de comissão, etc.
    '''
    serializer_class = ParlamentaresSerializer

    def get_queryset(self):
        # Reduz tabela para apenas um registro para cada parlamentar
        parlamentares_unicos = Atores.objects.filter(id_autor=OuterRef('id_autor')).distinct('id_autor')

        return Atores.objects.values('id_autor').annotate(total_documentos=Sum('num_documentos'),
                                                          peso_documentos=Sum('peso_total_documentos'),
                                                          nome=Subquery(parlamentares_unicos.values('nome_autor')),
                                                          partido=Subquery(parlamentares_unicos.values('partido')),
                                                          uf=Subquery(parlamentares_unicos.values('uf')),
                                                          casa=Subquery(parlamentares_unicos.values('casa')),
                                                          bancada=Subquery(parlamentares_unicos.values('bancada')))