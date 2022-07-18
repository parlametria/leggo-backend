from django.db.models import Q, Sum
from rest_framework import viewsets
from rest_framework.response import Response
from api.model.entidade import Entidade
from api.model.interesse import Interesse
from api.model.etapa_proposicao import Proposicao
from rest_framework import status
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from tweets.models import (
    EngajamentoProposicao,
    ParlamentarPerfil,
    Pressao,
    Tweet,
    TweetsInfo
)
from .serializers import RequisicaoFalha
from .serializers import (
    ParlamentarPerfilSerializer,
    TweetInteressesSerializer,
    TweetsInfoSerializer,
    PressaoSerializer,
    EngajamentoSerializer
)


class ParlamentarPefilViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        def get_parlamentar_or_false(pk):

            try:
                todas_legislaturas_casas = Entidade.objects.filter(
                    id_entidade_parlametria=pk)
                entidade = todas_legislaturas_casas.reverse().first()
                perfil = ParlamentarPerfil.objects.get(entidade=entidade)

                return perfil
            except (ParlamentarPerfil.DoesNotExist, Entidade.DoesNotExist):
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
            rf = RequisicaoFalha(e, request, pk)
            return rf.response()


class TweetsInfoViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            tweets_info = TweetsInfo().processa_atual_info()
            serializer = TweetsInfoSerializer(tweets_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            rf = RequisicaoFalha(e, request)
            return rf.response()


class TweetsViewSet(viewsets.ViewSet):

    def _get_interesses(self):
        interesses = Interesse.objects.all()
        distinct = interesses.distinct("interesse",
                                       "nome_interesse",
                                       "descricao_interesse")
        return distinct.values_list('interesse', 'proposicao')

    def retrieve(self, request, pk=None):
        self.interesses_tweets = {}
        self.ti_lista = []

        try:
            self.interesses_distintos = self._get_interesses()
            author = ParlamentarPerfil.objects.get(entidade=pk)

            """
            Para cada interesse UNICO, pego os interesses derivados e 
            suas respectivas proposicoes 
            """
            for i_distinto in self.interesses_distintos:
                interesse = i_distinto[0]
                interesses = Interesse.objects.filter(
                    Q(interesse=interesse) |
                    Q(nome_interesse=interesse) |
                    Q(descricao_interesse=interesse)
                ).values_list('proposicao')

                proposicoes = Proposicao.objects.filter(
                    id__in=interesses).values_list('id')

                self.interesses_tweets[interesse] = Tweet.objects.filter(
                    Q(author=author)
                    & Q(proposicao__id__in=proposicoes))

                if(self.interesses_tweets[interesse]):
                    ti = {"interesse": interesse,
                          "tweets": self.interesses_tweets[interesse]}

                    self.ti_lista.append(ti)

            serializer = TweetInteressesSerializer(self.ti_lista, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            rf = RequisicaoFalha(e, request, pk)
            return rf.response()

    def create(self, request):
        try:
            return Response({"data": json.dumps(request.data)},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            rf = RequisicaoFalha(e, request)
            return rf.response()


class PressaoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            proposicao = Proposicao.objects.get(id=pk)
            queryset = Pressao.objects.get(proposicao=proposicao)
            serializer = PressaoSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            rf = RequisicaoFalha(e, request, pk)
            return rf.response()

    def create(self, request):

        try:
            data = request.data
            convert_date = datetime.strptime(
                data.get('end_time'), '%Y-%m-%d')
            pressao = Pressao()
            pressao.proposicao = Proposicao.objects.get(id=data.get('proposicao'))
            pressao.data_consulta = convert_date
            pressao.save()

            return Response({"message": "OK", "data": ""},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            rf = RequisicaoFalha(e, request)
            return rf.response()


class EngajamentoViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):

        try:
            entidade = Entidade.objects.get(id=pk)
            parlamentar = ParlamentarPerfil.objects.get(entidade=entidade)
            queryset = EngajamentoProposicao.objects.filter(
                perfil=parlamentar).order_by('data_consulta')

            periodos = queryset.dates('data_consulta', 'month')
            lista_engajamentos = []
            for item in periodos:
                inicial = item
                final = (item + relativedelta(months=1))-timedelta(days=1)
                soma = queryset.filter(data_consulta__range=[inicial, final]).aggregate(
                    Sum('total_engajamento'))
                model = {
                    "total_engajamento": soma["total_engajamento__sum"],
                    "data_consulta": item
                }
                lista_engajamentos.append(model)

            serializer = EngajamentoSerializer(lista_engajamentos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            rf = RequisicaoFalha(e, request, pk)
            return rf.response()

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
            engajamento.data_consulta = convert_date.date()
            engajamento.proposicao = proposicao
            engajamento.save()

            serializer = EngajamentoSerializer(engajamento)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            rf = RequisicaoFalha(e, request)
            return rf.response()
