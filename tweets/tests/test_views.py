from rest_framework.test import APIClient
from django.test import TestCase
from api.model.entidade import Entidade
from api.model.interesse import Interesse
from api.model.etapa_proposicao import Proposicao
from tweets.models import EngajamentoProposicao, ParlamentarPerfil, Pressao, Tweet
from tweets.views import TweetsViewSet
from tweets.signals import procura_parlamentares_sem_perfil
from tweets.tests.test_models import Setup
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

    def test_retrieve_um(self):
        """
        Tweets de um interesses de um parlamentar
        """

        Setup().create_tweets()
        tweets = TweetsViewSet()
        interesse = 'outro'
        request_um = {
            'data': {
                'interesse': interesse
            }
        }

        pk = Setup().get_perfil().entidade

        novo_interesse = Interesse.objects.first()
        novo_interesse.interesse = interesse
        novo_interesse.save()

        tweets_freixo = Tweet.objects.filter(author=Setup().get_perfil())
        for tweet in tweets_freixo:
            tweet.proposicao.add(novo_interesse.proposicao)
            tweet.save()

        tweets.retrieve(request_um, pk=pk)

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

    def test_retrieve_tudo(self):
        """
        Tweets de todos os interesses de um parlamentar
        """

        Setup().create_tweets()
        tweets = TweetsViewSet()

        request_tudo = {
            'data': {
                'interesse': 'tudo'
            }
        }

        pk = Setup().get_perfil().entidade
        tweets.retrieve(request_tudo, pk=pk)

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

        # print(tweets.tweets_user.count())
        # print(tweets.tweets_user)

        # for t in Tweet.objects.all()[:4]:
        #     # print(t.proposicao.id)
        #     print(t.__dict__)
        #     print(t.author.name) if t.author else print('Sem perfil')

        # self.assertTrue(False)

#     def test_request(self):
#         n_results = 20
#         end = "2022-05-12T14:44:52.000Z"
#         start = "2022-05-10T14:44:52.000Z"
#         data = {
#             "search": "Você tem menos de 25 anos? Então nunca viu uma inflação como essa. O aumento foi puxado pela explosão nos preços da comida, do transporte e também pela alta no combustível. Desse jeito a gasolina do Bolsonaro vai chegar a R$10.",
#             "id_proposicao": f'{Proposicao.objects.all().first().id}',
#             "end_time":  f"{end}",
#             "start_time": f"{start}",
#             "n_results": f"{n_results}"
#         }

#         client = APIClient()

#         response = client.post(
#             "/tweets/",
#             json.dumps(data),
#             content_type="application/json",
#         )

#         tweets = Tweet.objects.all()
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(tweets.count(), n_results)
#         Setup.test_tweets_range(self, end, start, tweets)


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
    ENDPOINT = '/parlamentar-perfil/'

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
