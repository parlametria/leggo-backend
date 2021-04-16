from django.http import JsonResponse
from rest_framework import serializers, generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime
from api.model.pressao import Pressao
from api.utils.filters import get_filtered_interesses
from api.utils.queries_temp_pressao import queryPressaoOitoDias


class PressaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pressao
        fields = (
            'date', 'trends_max_pressao_principal',
            'trends_max_pressao_rel',	'trends_max_popularity',
            'twitter_mean_popularity', 'popularity')


class PressaoList(generics.ListAPIView):
    '''
    A partir do id da proposição no Sistema leggo, recupera histório da pressão
    com as informações da pesquisa no Google Trends e a popularidade da proposição
    no Twitter.
    '''

    serializer_class = PressaoSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id_leggo',
                openapi.IN_PATH,
                'id da proposição no sistema',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get_queryset(self):
        '''
        Retorna a pressão de uma proposição de um interesse em um período
        '''

        id_leggo = self.kwargs['id_leggo']
        interesseArg = self.request.query_params.get('interesse')
        data_inicio = self.request.query_params.get("data_inicio", None)
        data_fim = self.request.query_params.get("data_fim", None)

        interesses = get_filtered_interesses(interesseArg)

        data_inicio_processada = None
        data_fim_processada = None

        try:
            if data_inicio is not None:
                data_inicio_processada = datetime.strptime(data_inicio, "%Y-%m-%d")
        except ValueError:
            return JsonResponse(
                {
                    "error": f"Data de início ({data_inicio}) inválida."
                    "Formato correto: yyyy-mm-dd"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            data_fim_processada = (
                datetime.today()
                if data_fim is None
                else datetime.strptime(data_fim, "%Y-%m-%d")
            )
        except ValueError:
            print(
                f"Data de fim ({data_fim}) inválida. "
                "Utilizando data atual como data de fim."
            )
            data_fim_processada = datetime.today()

        queryset = Pressao.objects.filter(
            proposicao__id_leggo=id_leggo, interesse=interesseArg)

        if data_inicio_processada is not None:
            queryset = queryset.filter(date__gte=data_inicio_processada)

        queryset = queryset.filter(date__lte=data_fim_processada)

        queryset = (
            queryset.filter(
                proposicao__id_leggo__in=interesses.values("id_leggo")
            )
            .order_by("-date")
        )

        return queryset


class UltimaPressaoSerializer(serializers.Serializer):
    id_leggo = serializers.CharField()
    ultima_pressao = serializers.FloatField(source="trends_max_popularity")
    pressao_oito_dias = serializers.FloatField()


class UltimaPressaoList(generics.ListAPIView):
    '''
    Retorna a última pressão capturada para as proposições de um interesse e
    a última pressão em quinze dias.
    '''

    serializer_class = UltimaPressaoSerializer

    def get_queryset(self):
        '''
        Retorna a última pressão capturada para as proposições de um interesse
        e a ultima pressão em quinze dias.
        '''

        interesse_arg = self.request.query_params.get('interesse')

        if interesse_arg is None:
            interesse_arg = 'leggo'

        q = queryPressaoOitoDias(interesse_arg)

        pressao_oito_dias = Pressao.objects.raw(q)

        return pressao_oito_dias
