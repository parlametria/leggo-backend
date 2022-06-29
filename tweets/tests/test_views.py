from rest_framework.test import APIClient
from django.test import TestCase
from api.model.entidade import Entidade
from api.model.interesse import Interesse
from api.model.etapa_proposicao import Proposicao
from tweets.models import EngajamentoProposicao, ParlamentarPerfil, Pressao, Tweet
from tweets.views import TweetsViewSet
from tweets.signals.tweets_info import procura_parlamentares_sem_perfil
from tweets.tests.test_models import Setup
from types import SimpleNamespace
from datetime import datetime, timedelta
from unittest import skip
import json


class TestTweets(TestCase):
    fixtures = [
        "proposicoes.json",
        "interesses.json"
    ]

    def setUp(self):
        Setup().create_entidades()
        Setup().create_perfils()
        Setup().create_proposicao()

    def test_list_um_interesse(self):
        """
        Tweets de um interesses de um parlamentar
        """

        interesse = 'outro'
        request_um = {
            'query_params': {
                'interesse': interesse,
                'parlamentar': Setup().get_perfil().entidade.id

            }
        }
        Setup().create_tweets()

        request = SimpleNamespace(**request_um)
        tweets = TweetsViewSet()

        novo_interesse = Interesse.objects.first()
        novo_interesse.interesse = interesse
        novo_interesse.save()

        tweets_freixo = Tweet.objects.filter(author=Setup().get_perfil())
        for tweet in tweets_freixo:
            tweet.proposicao.add(novo_interesse.proposicao)
            tweet.save()

        tweets.list(request=request)

        self.assertTrue(
            tweets.proposicoes.filter(id=novo_interesse.proposicao.id).exists()
        )

        self.assertTrue(
            tweets.interesses.filter(id=novo_interesse.id).exists()
        )

        self.assertQuerysetEqual(
            tweets.tweets_user.order_by('id'),
            Tweet.objects.filter(author=Setup().get_perfil()).order_by('id')
        )

    def test_list_todos_interesses(self):
        """
        Tweets de todos os interesses de um parlamentar
        """

        Setup().create_tweets()
        tweets = TweetsViewSet()

        request_tudo = {
            'query_params': {
                'interesse': 'tudo',
                'parlamentar':  Setup().get_perfil().entidade.id
            }
        }
        request = SimpleNamespace(**request_tudo)
        tweets.list(request)

        self.assertQuerysetEqual(
            tweets.interesses.order_by('id'),
            Interesse.objects.all().order_by('id').values_list('id')
        )

        self.assertQuerysetEqual(
            tweets.proposicoes.order_by('id'),
            Proposicao.objects.all().order_by('id').values_list('id')
        )

        self.assertQuerysetEqual(
            tweets.tweets_user.order_by('id'),
            Tweet.objects.filter(author=Setup().get_perfil()).order_by('id')
        )

    def test_requisicao_list(self):
        """
        Endpoint tweets de todos os interesses de um parlamentar
        """

        Setup().create_tweets()

        request_tudo = {
            'data': {
                'interesse': 'tudo'
            }
        }

        parlamentar = Setup().get_perfil().entidade

        path = f'/tweets/?interesse=tudo&parlamentar={parlamentar.id}'
        client = APIClient()
        response = client.get(path)

        self.assertEqual(200, response.status_code)

    def test_retrieve(self):
        setup = Setup()
        Interesse.objects.all().delete()
        prop_1 = '3'
        prop_2 = '4'
        setup.create_tweets_diferente_interesses(prop_1, prop_2)

        views = TweetsViewSet()
        pk = setup.get_perfil().entidade.id

        views.retrieve(None, pk=pk)

        self.assertEqual(
            views.interesses_distintos[0][0],
            Interesse.objects.first().interesse)

        self.assertEqual(
            views.interesses_distintos[1][0],
            Interesse.objects.last().interesse)

        self.assertQuerysetEqual(
            views.interesses_tweets[Interesse.objects.first().interesse].order_by('id'),
            Tweet.objects.filter(proposicao__id_leggo__in=prop_1).order_by('id'))

        self.assertQuerysetEqual(
            views.interesses_tweets[Interesse.objects.last().interesse].order_by('id'),
            Tweet.objects.filter(proposicao__id_leggo__in=prop_2).order_by('id'))

        path = f'/tweets/{setup.get_perfil().entidade.id}/'
        client = APIClient()
        response = client.get(path)

        self.assertEqual(200, response.status_code)


class TestTweetsInfo(TestCase):
    fixtures = [
        'proposicoes.json',
        'entidades.json',
        'tweets-dump.json'
    ]

    def setUp(self):
        pass

    def test_get(self):
        path = '/tweets/info/'
        client = APIClient()
        response = client.get(path)

        data = response.data
        tweets = Tweet.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["numero_parlamentares_sem_perfil"],
                         procura_parlamentares_sem_perfil()[0])
        self.assertEqual(data["tweet_mais_novo"], tweets.reverse().first().data_criado)
        self.assertEqual(data["tweet_mais_antigo"], tweets.first().data_criado)
        self.assertEqual(data["numero_total_tweets"], tweets.count())


class TestPerfilParlamentar(TestCase):
    ENDPOINT = '/parlamentar/'

    def setUp(self):
        Setup().geral_setup()

    def test_perfil_retrieve(self):
        client = APIClient()

        flavio_bolsonaro = "25894"
        twitter_id = '40053694'

        path = f"{self.ENDPOINT}{flavio_bolsonaro}/"

        response = client.get(path)

        data = response.data
        self.assertEqual(None, data)

        Setup().create_perfil(flavio_bolsonaro, twitter_id, 'Flavio Bolsonaro')

        response = client.get(path)
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEquals(data.get('entidade'), int(flavio_bolsonaro))
        self.assertIsNotNone(data.get('twitter_id'))


class TestPressao(TestCase):
    ENDPOINT = '/pressao/'

    def setUp(self):
        Setup().geral_setup()

    def test_pressao_post(self):

        data = {
            "proposicao": Setup().get_preposicao().id,
            "end_time": Setup().end,
        }

        client = APIClient()
        response = client.post(
            f"{self.ENDPOINT}",
            json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_pressao_get(self):
        proposicao = Setup().get_preposicao()
        Setup().create_pressao()

        client = APIClient()

        response = client.get(
            f"{self.ENDPOINT}{proposicao.id}/",
        )
        data = response.data
        self.assertEqual(data.get('total_likes'), 70)
        self.assertEqual(data.get('total_engajamento'), 345)
        self.assertEqual(data.get('total_usuarios'), 2)
        self.assertEqual(data.get('total_tweets'), 10)


class TestEngajamento(TestCase):
    ENDPOINT = '/engajamento/'

    def setUp(self):
        Setup().geral_setup()

    def test_engajamento_post(self):

        Setup().create_pressao()

        data = {
            "proposicao": Setup().get_preposicao().id,
            "end_time": Setup().end,
            "twitter_id": Setup().marcelo.tid
        }

        client = APIClient()
        response = client.post(
            f"{self.ENDPOINT}",
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_invalido_post(self):

        data = {
            "proposicao": Setup().get_preposicao().id,
            "end_time": Setup().end,
            "twitter_id": Setup().jair.tid
        }

        client = APIClient()
        response = client.post(
            f"{self.ENDPOINT}",
            json.dumps(data),
            content_type="application/json",
        )

        # O test vai apresentar Bad request, mas está OK. Queremos que falhe mesmo
        self.assertEqual(response.status_code, 400)

    def test_engajamento_get(self):

        autor = Setup().get_perfil()
        Setup().create_pressao()
        Setup().create_engajamento()

        client = APIClient()

        response = client.get(
            f"{self.ENDPOINT}?twitter_id={autor.twitter_id}&proposicao={Setup().get_preposicao().id}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('total_engajamento'), 120)
