from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProposicaoList(APIView):
    """
    """
    def get(self, request, format=None):
        # snippets = Snippet.objects.all()
        # serializer = SnippetSerializer(snippets, many=True)
        # return Response(serializer.data)
        return Response(['bom dia', 'boa tarde', 'boa noite'])
