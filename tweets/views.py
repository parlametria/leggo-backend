from cProfile import Profile
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from api.model.entidade import Entidade
from tweets.models import Engajamento, ParlamentarPerfil, Pressao, Proposicao, Tweet
from api.model.interesse import Interesse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
import logging
import traceback
import json
from .serializers import *
from django.db.models import Subquery


class ParlamentarPefilViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        def get_parlamentar_or_false(pk):
            try:
                entidade = Entidade.objects.get(id_entidade_parlametria=pk)
                perfil = ParlamentarPerfil.objects.get(entidade=entidade)

                return perfil
            except ParlamentarPerfil.DoesNotExist as e:
                return False

        try:
            perfil = get_parlamentar_or_false(pk)
            # Entidade.objects.filter(id_entidade_parlametria="25894")
            if(perfil):
                serializer = ParlamentarPerfilSerializer(perfil)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"mensagem": "O perfil do parlamentar não foi encontrado", "pk": pk, "twitter_id": None}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"mensagem": f"{e}", "pk": pk}, status=status.HTTP_400_BAD_REQUEST)


class TweetsViewSet(viewsets.ViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def list(self, request):
        return Response('GET')

    def retrieve(self, request, pk=None):
        data = request.get('data')
        interesse = data.get('interesse')

        def get_interesses():
            if(interesse == 'todo'):
                return Interesse.objects.all().values_list('id')
            return Interesse.objects.filter(interesse=interesse).values_list('id')

        def get_proposicoes_por_intesses():
            interesses = get_interesses()
            propos = Proposicao.objects.filter(id__in=interesses)
            return propos

        get_proposicoes_por_intesses()

        def get_tweets_por_interesse(twitter_id):
            Tweet.objects.filter(proposicao__in=Subquery())
            pass

        pass

        return Response({"pk": pk, "interesse": 'teste'}, status=status.HTTP_201_CREATED)

    def create(self, request):
        data = request.data

        try:
            return Response({"data": json.dumps(request.data)}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"erro": f"{e}", "data": json.dumps(request.data)}, status=status.HTTP_400_BAD_REQUEST)


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
                return ParlamentarPerfil.objects.get(twitter_id=twitter_id)
            except ParlamentarPerfil.DoesNotExist as e:
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
