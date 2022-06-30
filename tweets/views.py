from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from yaml import serialize
from api.model.entidade import Entidade
from tweets.models import EngajamentoProposicao, ParlamentarPerfil, Pressao, Tweet, TweetsInfo
from api.model.interesse import Interesse
from api.model.etapa_proposicao import Proposicao
from rest_framework import status
from datetime import datetime, timedelta
import traceback
import json
from .serializers import *


class ParlamentarPefilViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        def get_parlamentar_or_false(pk):

            try:
                todas_legislaturas_casas = Entidade.objects.filter(
                    id_entidade_parlametria=pk)
                entidade = todas_legislaturas_casas.reverse().first()
                perfil = ParlamentarPerfil.objects.get(entidade=entidade)

                return perfil
            except (ParlamentarPerfil.DoesNotExist, Entidade.DoesNotExist) as e:
                return False

        try:
            perfil = get_parlamentar_or_false(pk)
            # Entidade.objects.filter(id_entidade_parlametria="25894")
            if(perfil):
                serializer = ParlamentarPerfilSerializer(perfil)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                tweets_info = TweetsInfo().processa_atual_info()
                serializer = TweetsInfoSerializer(tweets_info)

                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"mensagem": f"{e}", "pk": pk}, status=status.HTTP_400_BAD_REQUEST)


class TweetsInfoViewSet(viewsets.ViewSet):
    def list(self, request):
        tweets_info = TweetsInfo().processa_atual_info()
        serializer = TweetsInfoSerializer(tweets_info)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TweetsViewSet(viewsets.ViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def retrieve(self, request, pk=None):
        self.interesses_tweets = {}
        self.ti_lista = []

        class TweetsInteresse(object):
            def __init__(self, interesse, tweets):
                self.interesse = interesse
                self.tweets = tweets

        try:
            def get_interesses():
                return Interesse.objects.all().distinct("interesse", "nome_interesse",
                                                        "descricao_interesse").values_list('interesse', 'proposicao')
            self.interesses_distintos = get_interesses()
            author = ParlamentarPerfil.objects.get(entidade=pk)

            """
            Para cada interesse UNICO, pego os interesses derivados e suas respectivas proposicoes 
            """
            for i_distinto in self.interesses_distintos:
                print(i_distinto[0])
                interesses = Interesse.objects.filter(
                    Q(interesse=i_distinto[0]) |
                    Q(nome_interesse=i_distinto[0]) |
                    Q(descricao_interesse=i_distinto[0])
                ).values_list('id', 'proposicao')

                proposicoes = Proposicao.objects.filter(
                    id__in=interesses[0]).values_list('id')

                self.interesses_tweets[i_distinto[0]] = Tweet.objects.filter(
                    Q(author=author)
                    & Q(proposicao__id__in=proposicoes))

                ti = TweetsInteresse(i_distinto[0],
                                     self.interesses_tweets[i_distinto[0]])
                self.ti_lista.append(ti)

            serializer = TweetInteressesSerializer(self.ti_lista, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            print(traceback.format_exc())
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        try:
            parlamentar = request.query_params.get('parlamentar')
            interesse = request.query_params.get('interesse')

            def get_interesses():
                if(interesse in ['tudo', 'todo', 'todos', 'all']):
                    return Interesse.objects.all().values_list('id')
                return Interesse.objects.filter(interesse=interesse).values_list('id')

            def get_proposicoes_por_intesses(interesses):
                propos = Proposicao.objects.filter(id__in=interesses).values_list('id')
                return propos

            def get_tweets_por_proposicao(proposicoes):
                author = ParlamentarPerfil.objects.get(entidade=parlamentar)
                tweets = Tweet.objects.filter(
                    Q(proposicao__id__in=proposicoes) & Q(author=author))
                return tweets

            self.interesses = get_interesses()
            self.proposicoes = get_proposicoes_por_intesses(self.interesses)
            self.tweets_user = get_tweets_por_proposicao(self.proposicoes)

            serializer = TweetSerializer(
                self.tweets_user, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            print(traceback.format_exc())
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

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

    def retrieve(self, request, pk=None):
        try:
            entidade = Entidade.objects.get(id=pk)
            parlamentar = ParlamentarPerfil.objects.get(entidade=entidade)
            queryset = EngajamentoProposicao.objects.filter(
                perfil=parlamentar)

            serializer = EngajamentoSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            print(traceback.format_exc())
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):

        try:
            data = request.query_params
            proposicao = Proposicao.objects.get(id=data.get('proposicao'))
            queryset = EngajamentoProposicao.objects.get(
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
            engajamento = EngajamentoProposicao()
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
