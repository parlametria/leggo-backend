from api.model.entidade import Entidade
from api.model.etapa_proposicao import EtapaProposicao
from api.model.proposicao import Proposicao
from api.model.interesse import Interesse
from django.test import TestCase
from django.contrib.auth.models import User
from usuario.models import UsuarioProposicao
from api import signals
from tweets.models import Engajamento, Perfil, Pressao, Proposicao, Tweet
from datetime import datetime, timedelta
from .setup import Setup


class PerfilTests(TestCase):
    def setUp(self):
        setup = Setup()
        setup.create_entidades()

    def test_populate(self):
        setup = Setup()
        perfil = Perfil()
        perfil.populate_parlamentar()
        self.assertTrue(Perfil.objects.get(entidade_id=setup.jair.eid))
        self.assertTrue(Perfil.objects.get(entidade_id=setup.marcelo.eid))


# class TweetsTest(TestCase):
#     def setUp(self):
#         setup = Setup(["jairbolsonaro"])
#         setup.create_entidades()
#         setup.create_perfils()
#         setup.create_proposicao()

    # def test_req(self):
    #     tweet = Tweet()

    #     data = {
    #         "search": "Mesmo antes da pandemia, já em 2019 foram batidos mais recordes, desta vez, de abertura de leitos hospitalares:",
    #         "id_proposicao": Proposicao.objects.all()[0].id,
    #         "end_time":  datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
    #         "start_time": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
    #         "n_results": "30"
    #     }

    #     print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'))
    #     print((datetime.now() - timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S.000Z'))

    #     search = "Mesmo antes da pandemia, já em 2019 foram batidos mais recordes, desta vez, de abertura de leitos hospitalares"
    #     tweet.get_recent(search, Proposicao.objects.all()[
    #                      0].id, datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
    #                      (datetime.now() - timedelta(days=2)
    #                       ).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    #                      )


class PressaoTests(TestCase):
    def setUp(self):
        setup = Setup()
        setup.create_entidades()
        setup.create_perfils()
        setup.create_proposicao()
        setup.create_tweets()

    def test_pressao(self):
        setup = Setup()
        pressao = Pressao()
        pressao.proposicao = setup.get_preposicao()
        pressao.data_consulta = setup.end_c
        pressao.save()

        self.assertEqual(pressao.total_likes, 70)
        self.assertEqual(pressao.total_engajamento, 345)
        self.assertEqual(pressao.total_usuarios, 2)
        self.assertEqual(pressao.total_tweets, 10)
        self.assertTrue(setup.test_tweets_range(pressao.get_tweets()))


class EngajamentoTests(TestCase):
    def setUp(self):
        setup = Setup()
        setup.create_entidades()
        setup.create_perfils()
        setup.create_proposicao()
        setup.create_tweets()

    def test_engajamento(self):
        setup = Setup()
        engajamento = Engajamento()
        engajamento.perfil = Perfil.objects.get(twitter_id=setup.marcelo.tid)
        engajamento.data_consulta = setup.end_c
        engajamento.proposicao = setup.get_preposicao()
        engajamento.save()
        self.assertEqual(engajamento.total_engajamento, 120)
        self.assertTrue(setup.test_tweets_range(engajamento.get_tweets()))
