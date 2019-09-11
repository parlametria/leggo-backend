from rest_framework import serializers

class Info(APIView):
    '''
    Informações gerais sobre a plataforma.
    '''

    def get(self, request, format=None):
        return Response({i.name: i.value for i in InfoGerais.objects.all()})



