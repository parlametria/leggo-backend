from rest_framework import serializers, generics
from api.views.interesse_serializer import InteresseSerializer
from api.model.tramitacao_event import TramitacaoEvent
from api.utils.presidencia_comissao import (
    get_comissao_parlamentar,
    get_comissao_parlamentar_id)

class PresidenciaComissaoSerializer(serializers.Serializer):

    id_autor = serializers.IntegerField()
    id_comissao = serializers.IntegerField()
    id_autor_voz = serializers.IntegerField()
    quantidade_comissao_presidente = serializers.IntegerField()
    info_comissao = serializers.CharField()
    interesse = InteresseSerializer(many=True, read_only=True)

class PresidenciaComissaoLista(generics.ListAPIView):
    serializer_class = PresidenciaComissaoSerializer

    def get_queryset(self):

        '''
        Retorna informações sobre os parlamentares presidentes de comissões que
        passaram por tramitação.
        '''
        interesseArg = self.request.query_params.get("interesse")

        if interesseArg is None:
            interesseArg = "leggo"

        consultaTramitacao = TramitacaoEvent.objects.raw("SELECT distinct(sigla_local) as id FROM api_tramitacaoevent "

            + "LEFT JOIN api_etapaproposicao as etapa ON etapa_proposicao_id = etapa.id "

            + "LEFT JOIN api_proposicao as prop ON proposicao_id = prop.id "

            + "LEFT JOIN api_interesse as interesse ON prop.id = interesse.id "

            + "WHERE interesse.interesse = %s ", [interesseArg])

        listaComissoesPassadas = []

        for obj in consultaTramitacao:
            listaComissoesPassadas.append(obj.id)

        data = get_comissao_parlamentar(listaComissoesPassadas)

        return data

class PresidenciaComissaoParlamentar(generics.ListAPIView):

    serializer_class = PresidenciaComissaoSerializer

    def get_queryset(self):

        '''Retorna informações sobre os parlamentares presidentes de comissões de
        acordo com o id.'''
        interesseArg = self.request.query_params.get("interesse")

        if interesseArg is None:
            interesseArg = "leggo"

        consultaTramitacao = TramitacaoEvent.objects.raw("SELECT distinct(sigla_local) as id FROM api_tramitacaoevent "

            + "LEFT JOIN api_etapaproposicao as etapa ON etapa_proposicao_id = etapa.id "

            + "LEFT JOIN api_proposicao as prop ON proposicao_id = prop.id "

            + "LEFT JOIN api_interesse as interesse ON prop.id = interesse.id "

            + "WHERE interesse.interesse = %s ", [interesseArg])

        listaComissoesPassadas = []

        for obj in consultaTramitacao:
            listaComissoesPassadas.append(obj.id)

        id_autor_arg = self.kwargs["id"]

        return get_comissao_parlamentar_id(id_autor_arg, listaComissoesPassadas)
