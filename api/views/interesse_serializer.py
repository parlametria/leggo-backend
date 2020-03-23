from rest_framework import serializers, generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.model.interesse import Interesse


class InteresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interesse
        fields = (
            'id_leggo', 'interesse')


class InteresseList(generics.ListAPIView):
    '''
    Dados de mapeamento entre interesse e proposições
    '''

    serializer_class = InteresseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema do Leg.go',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        '''
        Retorna interesses associados a uma PL
        '''
        id_prop = self.kwargs['id']
        return Interesse.objects.filter(id_leggo=id_prop)
