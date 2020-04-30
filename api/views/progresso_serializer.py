from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.progresso import Progresso
from datetime import datetime


class ProgressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progresso
        fields = ('fase_global', 'local', 'data_inicio',
                  'data_fim', 'local_casa', 'pulou')


class ProgressoList(generics.ListAPIView):
    '''
    Dados do progresso da proposição por período, de acordo com uma data de referência
    passada como parâmetro (?data_referencia=yyyy-mm-dd).
    '''
    serializer_class = ProgressoSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'casa', openapi.IN_PATH, 'casa da proposição', type=openapi.TYPE_STRING),
            openapi.Parameter(
                'id_ext', openapi.IN_PATH, 'id da proposição no sistema da casa',
                type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'data_referencia', openapi.IN_PATH,
                'data de referência a ser considerada',
                type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        '''
        Retorna o progresso de uma proposição, passando uma data de referência.
        '''
        casa = self.kwargs['casa']
        id_ext = self.kwargs['id_ext']
        data_referencia = self.request.query_params.get('data_referencia', None)
        queryset = Progresso.objects.filter(
            etapa__casa=casa, etapa__id_ext=id_ext)

        try:
            hoje = datetime.today() if data_referencia is None else datetime.strptime(
                data_referencia, '%Y-%m-%d')
        except ValueError:
            print(
                f'Data de referência ({data_referencia}) inválida. '
                'Utilizando data atual como data de referência.')
            hoje = datetime.today()

        if data_referencia is None:
            queryset = queryset.filter()
        else:
            queryset = queryset.filter(data_inicio__lte=hoje)

        return queryset
