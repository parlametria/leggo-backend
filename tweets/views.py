from cProfile import Profile
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from tweets.models import Engajamento, Perfil, Pressao, Proposicao, Tweet
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
import logging
import traceback


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tweet
        fields = ['proposicao', 'author', 'id_author', 'id_tweet',
                  'text', 'data_criado',  'likes', 'retweets', 'respostas']


class PressaoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pressao
        fields = [
            'total_likes',
            'total_tweets',
            'total_usuarios',
            'total_engajamento',
            'data_consulta',
        ]


class EngajamentoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Engajamento
        fields = [
            'data_consulta',
            'total_engajamento',
        ]


class TweetsViewSet(viewsets.ViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def list(self, request):
        return Response('GET')

    def create(self, request):
        data = request.data

        try:
            tweet = Tweet()
            tweet.get_recent(data.get("search"),
                             id_proposicao=data.get('id_proposicao'),
                             start_time=data.get('start_time'),
                             end_time=data.get('end_time'),
                             n_results=data.get('n_results'))

            return Response({"message": "OK", "data": ""}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"message": f"Some error:\n {e}", "data": ""}, status=status.HTTP_400_BAD_REQUEST)


class PressaoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            proposicao = Proposicao.objects.get(id=pk)
            queryset = Pressao.objects.get(proposicao=proposicao)
            serializer = PressaoSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"message": f"{e}", "data": {"pk": pk}}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):

        try:
            data = request.data
            convert_date = datetime.strptime(
                data.get('end_time'), '%Y-%m-%d')
            pressao = Pressao()
            pressao.proposicao = Proposicao.objects.get(id=data.get('proposicao'))
            pressao.data_consulta = convert_date
            pressao.save()

            return Response({"message": "OK", "data": ""}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"message": f"{e}", "data": ""}, status=status.HTTP_400_BAD_REQUEST)


class EngajamentoViewSet(viewsets.ViewSet):

    def list(self, request):

        try:
            data = request.query_params
            proposicao = Proposicao.objects.get(id=data.get('proposicao'))
            queryset = Engajamento.objects.get(
                proposicao=proposicao,
                tid_author=data.get('twitter_id'))
            serializer = EngajamentoSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(traceback.format_exc())
            message = {"message": f"{e}",
                       "proposicao:": data.get('proposicao'),
                       "twitter_id": data.get('twitter_id')}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):

        def get_perfil(twitter_id):
            try:
                return Perfil.objects.get(twitter_id=twitter_id)
            except Perfil.DoesNotExist as e:
                return None

        try:
            data = request.data
            proposicao = Proposicao.objects.get(id=data.get('proposicao'))
            convert_date = datetime.strptime(data.get('end_time'),
                                             '%Y-%m-%d')
            engajamento = Engajamento()
            engajamento.perfil = get_perfil(data.get('twitter_id'))
            engajamento.tid_author = data.get('twitter_id')
            engajamento.data_consulta = convert_date
            engajamento.proposicao = proposicao
            engajamento.save()

            serializer = EngajamentoSerializer(engajamento)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # print(traceback.format_exc())
            message = {"message": f"{e}",
                       "proposicao:": data.get('proposicao'),
                       "twitter_id": data.get('twitter_id')}

            return Response(message, status=status.HTTP_400_BAD_REQUEST)
