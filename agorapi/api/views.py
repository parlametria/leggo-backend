from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils import props


class Info(APIView):
    '''
    Informações gerais sobre a plataforma.
    '''
    def get(self, request, format=None):
        return Response({'status': 'ok'})


class ProposicaoList(APIView):
    '''
    Lista de proposições.
    '''
    def get(self, request, format=None):
        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return Response(serializer.data)
        return Response(props.to_dict(orient='records'))
