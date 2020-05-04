from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.coautoria_edge import CoautoriaEdge


class CoautoriaEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoautoriaEdge
        fields = ('source', 'target', 'value')


class CoautoriaEdgeList(generics.ListAPIView):
    '''
    A partir de uma proposição lista ligações (arestas) entre os parlamentares
    que apresentaram documentos relacionados à proposição.
    '''
    serializer_class = CoautoriaEdgeSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs['id']
        return CoautoriaEdge.objects.filter(id_leggo=id_prop)
