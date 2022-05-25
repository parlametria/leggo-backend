from django.test import TestCase
from tweets.models import Engajamento, Perfil, Pressao, Tweet
from datetime import datetime, timedelta
from .setup import Setup
import json
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import skip


class PerfilTests(TestCase):
    def setUp(self):
        Setup().create_entidades()

    def test_populate(self):
        perfil = Perfil()
        perfil.populate_parlamentar()
        self.assertTrue(Perfil.objects.get(entidade_id=Setup().jair.eid))
        self.assertTrue(Perfil.objects.get(entidade_id=Setup().marcelo.eid))


class MockPage:
    def __init__(self, data):
        self.data = map(self.dict_to_tweet, data)

    def dict_to_tweet(self, item):
        return dotdict(item)


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# @skip('')
class TweetsTest(TestCase):
    def setUp(self):
        Setup().create_entidades()
        Setup().create_perfils()
        Setup().create_proposicao()
        json_file = open("./tweets/tests/tweets.json", 'r', encoding='utf-8')
        self.tweets = json.load(json_file)
        print('-'*30)
        print(self.tweets)

    def test_req(self):

        tweet = Tweet()

        mock = MockPage(self.tweets)
        pages = [
            mock
        ]

        tweet.get_recent = MagicMock(return_value=pages)
        req = tweet.get_recent()

        tweet.get_paginate(req, Setup().get_preposicao())
        self.assertEqual(Tweet.objects.all().count(), 10)


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

        engajamento = Engajamento()
        engajamento.perfil = Perfil.objects.get(twitter_id=Setup().marcelo.tid)
        engajamento.data_consulta = Setup().end_c
        engajamento.proposicao = Setup().get_preposicao()
        engajamento.save()
        self.assertEqual(engajamento.total_engajamento, 120)
        self.assertTrue(Setup().test_tweets_range(engajamento.get_tweets()))

    def test_nao_engajamento(self):
        engajamento = Engajamento()
        engajamento.perfil = Perfil.objects.get(twitter_id=Setup().jair.tid)
        engajamento.data_consulta = Setup().end_c
        engajamento.proposicao = Setup().get_preposicao()
        self.assertRaises(Exception, engajamento.save)
