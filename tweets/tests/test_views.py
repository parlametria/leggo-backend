from rest_framework.test import APIClient
from django.test import TestCase
from api.model.interesse import Interesse
from api.model.proposicao import Proposicao
from tweets.models import EngajamentoProposicao, ParlamentarPerfil, Tweet, TweetsInfo
from tweets.views import TweetsViewSet
from tweets.tests.test_models import Setup
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import json


class TestTweets(TestCase):

    def load_data(self):
        s = Setup()
        s.create_proposicao()
        proposicao = Proposicao.objects.all().first()
        file = open('./tweets/tests/mocked_airflow_tweets_req.json',
                    'r', encoding='utf-8')
        data = json.load(file)
        data['proposicao'] = proposicao.id
        return data

    def make_tweets_request(self, data):
        ENDPOINT = '/tweets/'
        client = APIClient()
        return client.post(
            f"{ENDPOINT}",
            json.dumps(data),
            content_type="application/json",
        )

    def setUp(self):
        s = Setup()
        s.create_entidades()
        s.create_perfils()

    def test_create(self):
        response = self.make_tweets_request(self.load_data())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tweet.objects.all().count(), 10)
        self.assertEqual(Tweet.objects.filter(
            author=ParlamentarPerfil.objects.all().last()).count(), 1)

    def test_create_atualiza_metricas(self):
        data = self.load_data()
        self.make_tweets_request(data)
        item = data['tweets'][0]
        item['respostas'] = 666
        data['tweets'][0] = item
        response = self.make_tweets_request(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tweet.objects.all().count(), 10)
        self.assertEqual(Tweet.objects.get(id_tweet=item['id_tweet']).respostas, 666)

    def test_create_atualiza_info(self):
        response = self.make_tweets_request(self.load_data())
        tweets = Tweet.objects.all()
        info = TweetsInfo.processa_atual_info()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(info.tweet_mais_novo, tweets.last())
        self.assertEqual(info.tweet_mais_antigo, tweets.first())

    def test_retrieve(self):
        setup = Setup()
        prop_1 = '3'
        prop_2 = '4'
        setup.create_tweets_diferente_interesses(prop_1, prop_2, setup.datas[0])

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

    def test_engajamento_retrieve(self):
        setup = Setup()
        autor = setup.get_perfil()
        EngajamentoProposicao.objects.all()
        Tweet.objects.all().delete()

        datas = [setup.end_c,
                 setup.end_c + timedelta(days=2),
                 setup.end_c + relativedelta(months=1)]

        setup.create_tweets_diferente_interesses(3, 4, datas[0])
        setup.create_tweets_diferente_interesses(5, 6, datas[1])
        setup.create_tweets_diferente_interesses(7, 8, datas[2])

        setup.create_engajamento_diferentes_proposicao(3, 4, datas[0])
        setup.create_engajamento_diferentes_proposicao(5, 6, datas[1])
        setup.create_engajamento_diferentes_proposicao(7, 8, datas[2])

        client = APIClient()

        response = client.get(
            f"{self.ENDPOINT}{autor.entidade.id}/",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        """
        Verifica se o engajamento mensal vai ser somado dos dias diferentes
        prop1 = 150, prop2 = 120, dias = 2
        (prop1+prop2) * 2 = 540
        """
        self.assertEqual(response.data[0]['total_engajamento'], 540)
        """
        O valor do proximo mês prop1+prop2
        """
        self.assertEqual(response.data[1]['total_engajamento'], 270)
