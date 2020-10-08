from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.pressao import Pressao
from api.utils.filters import get_filtered_interesses


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
                'id_leggo', openapi.IN_PATH, 'id da proposição no sistema',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna a pressão
        '''

        interesseArg = self.request.query_params.get('interesse')

        # Adiciona interesse default
        if interesseArg is None:
            interesseArg = 'leggo'

        id_leggo = self.kwargs['id_leggo']
        queryset = Pressao.objects.filter(
            proposicao__id_leggo=id_leggo, interesse=interesseArg)

        return queryset


class UltimaPressaoSerializer(serializers.Serializer):
    id_leggo = serializers.CharField()
    ultima_pressao = serializers.FloatField(source="trends_max_popularity")
    date = serializers.DateField()


class UltimaPressaoList(generics.ListAPIView):
    '''
    Retorna a última pressão capturada para as proposições de um interesse
    '''

    serializer_class = UltimaPressaoSerializer

    def get_queryset(self):
        '''
        Retorna a última pressão capturada para as proposições de um interesse
        '''

        interesse_arg = self.request.query_params.get('interesse')

        if interesse_arg is None:
            interesse_arg = 'leggo'

        interesses = get_filtered_interesses(interesse_arg)
        queryset = (
            Pressao.objects.filter(
                proposicao__id_leggo__in=interesses.values('id_leggo'))
            .values('id_leggo', 'trends_max_popularity', 'date')
            .order_by('id_leggo', '-date')
            .distinct('id_leggo')
        )

        return queryset
