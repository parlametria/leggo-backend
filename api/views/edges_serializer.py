from rest_framework import serializers, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.model.edges import Edges


class EdgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edges
        fields = ('source', 'target', 'value')


class EdgesList(generics.ListAPIView):
    '''
    Lista as edges
    '''
    serializer_class = EdgesSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, 'id da proposição no sistema',
                type=openapi.TYPE_INTEGER),
        ]
    )
    def get_queryset(self):
        id_prop = self.kwargs['id']
        return Nodes.objects.filter(id_leggo=id_prop)