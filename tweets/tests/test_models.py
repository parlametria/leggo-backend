from django.test import TestCase
from tweets.models import EngajamentoProposicao, ParlamentarPerfil, Pressao
from .setup import Setup


class PerfilTests(TestCase):
    def setUp(self):
        Setup().create_entidades()


class PressaoTests(TestCase):
    def setUp(self):
        Setup().geral_setup()

    def test_pressao(self):
        pressao = Pressao()
        pressao.proposicao = Setup().get_preposicao()
        pressao.data_consulta = Setup().end_c
        pressao.save()

        self.assertEqual(pressao.total_likes, 70)
        self.assertEqual(pressao.total_engajamento, 345)
        self.assertEqual(pressao.total_usuarios, 2)
        self.assertEqual(pressao.total_tweets, 10)
        self.assertTrue(Setup().test_tweets_range(pressao.get_tweets()))


class EngajamentoTests(TestCase):
    def setUp(self):
        Setup().geral_setup()

    def test_engajamento(self):
        engajamento = EngajamentoProposicao()
        engajamento.perfil = ParlamentarPerfil.objects.get(twitter_id=Setup().marcelo.tid)
        engajamento.data_consulta = Setup().end_c
        engajamento.proposicao = Setup().get_preposicao()
        engajamento.save()
        self.assertEqual(engajamento.total_engajamento, 120)
        self.assertTrue(Setup().test_tweets_range(engajamento.get_tweets()))

    def test_engajamento_sem_tweets(self):
        engajamento = EngajamentoProposicao()
        engajamento.perfil = ParlamentarPerfil.objects.get(twitter_id=Setup().jair.tid)
        engajamento.data_consulta = Setup().end_c
        engajamento.proposicao = Setup().get_preposicao()
        self.assertRaises(Exception, engajamento.save)

    def test_tweet_fora_range(self):
        """
        Test com tweets fora do intervalo.
        Testa se o filtro de data esta funcionando.
        """
        s = Setup()
        s.create_tweets_diferente_interesses(3, 4, s.end_c)
        s.create_engajamento_diferentes_proposicao(3, 4, s.end_c)
        engajamento = EngajamentoProposicao()
        engajamento.perfil = ParlamentarPerfil.objects.get(twitter_id=Setup().marcelo.tid)
        engajamento.data_consulta = Setup().end_c
        engajamento.proposicao = Setup().get_preposicao()
        engajamento.save()
        self.assertEqual(engajamento.total_engajamento, 120)
        self.assertTrue(Setup().test_tweets_range(engajamento.get_tweets()))
