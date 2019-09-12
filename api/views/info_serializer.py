from rest_framework.views import APIView
from rest_framework.response import Response
from api.model.info_geral import InfoGerais


class Info(APIView):
    '''
    Informações gerais sobre a plataforma.
    '''

    def get(self, request, format=None):
        return Response({i.name: i.value for i in InfoGerais.objects.all()})
