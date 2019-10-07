from rest_framework import serializers, generics
from api.views.pauta_serializer import PautaHistoricoSerializer
from api.model.etapa_proposicao import EtapaProposicao
from api.views.ator_serializer import AtoresSerializer, AtoresSerializerComissoes


class EtapasSerializer(serializers.ModelSerializer):
    pauta_historico = PautaHistoricoSerializer(many=True, read_only=True)

    class Meta:
        model = EtapaProposicao
        fields = (
            'id', 'id_ext', 'casa', 'sigla', 'data_apresentacao', 'ano', 'sigla_tipo',
            'regime_tramitacao', 'forma_apreciacao', 'ementa', 'justificativa', 'url',
            'autores', 'relator_nome', 'casa_origem',
            'em_pauta', 'apelido', 'tema', 'status', 'top_resumo_tramitacao',
            'ultima_pressao', 'comissoes_passadas',
            'pauta_historico', 'temas')


class EtapasDetailSerializer(serializers.ModelSerializer):
    pauta_historico = PautaHistoricoSerializer(many=True, read_only=True)
    top_atores = AtoresSerializer(many=True, read_only=True)
    top_important_atores = AtoresSerializerComissoes(many=True, read_only=True)

    class Meta:
        model = EtapaProposicao
        fields = (
            'id', 'id_ext', 'casa', 'sigla', 'data_apresentacao', 'ano', 'sigla_tipo',
            'regime_tramitacao', 'forma_apreciacao', 'ementa', 'justificativa', 'url',
            'autores', 'relator_nome', 'casa_origem',
            'em_pauta', 'apelido', 'tema', 'status', 'resumo_tramitacao', 'top_atores',
            'top_important_atores', 'comissoes_passadas',
            'pauta_historico', 'temas', 'ultima_pressao')


class EtapasList(generics.ListAPIView):
    '''
    Dados gerais da proposição.
    '''
    queryset = EtapaProposicao.objects.prefetch_related(
        'tramitacao', 'temperatura_historico')
    serializer_class = EtapasSerializer
