from rest_framework.test import APIClient
from django.test import TestCase
from tweets.models import Engajamento, Perfil, Pressao, Proposicao, Tweet
from tweets.tests.test_models import Setup
from datetime import datetime, timedelta
import json


# class TestTweets(TestCase):

#     def setUp(self):
#         Setup.create_proposicao(self)

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


class TestPressao(TestCase):
    ENDPOINT = '/pressao/'

    def setUp(self):
        setup = Setup()
        setup.create_entidades()
        setup.create_perfils()
        setup.create_proposicao()
        setup.create_tweets()

    def test_pressao_post(self):
        setup = Setup()

        data = {
            "proposicao": setup.get_preposicao().id,
            "end_time": setup.end,
        }

        client = APIClient()
        response = client.post(
            f"{self.ENDPOINT}",
            json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)

    def test_pressao_get(self):
        setup = Setup()
        proposicao = setup.get_preposicao()
        setup.create_pressao()

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
        setup = Setup()
        setup.create_entidades()
        setup.create_perfils()
        setup.create_proposicao()
        setup.create_tweets()

    def test_engajamento_post(self):
        setup = Setup()
        setup.create_pressao()

        data = {
            "proposicao": setup.get_preposicao().id,
            "end_time": setup.end,
            "twitter_id": setup.marcelo.tid
        }

        client = APIClient()
        response = client.post(
            f"{self.ENDPOINT}",
            json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_engajamento_get(self):
        setup = Setup()
        autor = setup.get_perfil()
        setup.create_pressao()
        setup.create_engajamento()

        client = APIClient()

        response = client.get(
            f"{self.ENDPOINT}?twitter_id={autor.twitter_id}&proposicao={setup.get_preposicao().id}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('total_engajamento'), 120)
