import json
from dotenv import dotenv_values
from api.model.entidade import Entidade
from tweets.models import ParlamentarPerfil, Tweet, TweetsInfo
from api.model.etapa_proposicao import Proposicao
from .setup import Setup
from django.test import TestCase
from api.signals import get_tweets
import uuid
import traceback
from tweets.signals.tweets_info import recupera_parlmanetares_casa, procura_parlamentares_sem_perfil
from datetime import datetime


class SignalTests(TestCase):
    def setUp(self):
        setup = Setup()
        setup.create_entidades()
        setup.create_perfils()

    def test_signal(self):
        id = str(uuid.uuid4())
        conflict = 409
        proposicao = Proposicao(id_leggo=id)
        proposicao.save()
        instance, response = get_tweets(Proposicao, proposicao, True)
        content = json.loads(response.content)
        self.assertEqual(proposicao.id_leggo, instance.id_leggo)
        self.assertEqual(content.get('status'), conflict)


class TwitterInfoTests(TestCase):
    fixtures = [
        "proposicoes.json",
        "interesses.json",
        "entidades.json"
    ]

    def setUp(self) -> None:
        senado = 'senado'
        camara = 'camara'
        self.CORRIGIR_SENADO = 1
        self.senadores = recupera_parlmanetares_casa(senado)
        self.deputados = recupera_parlmanetares_casa(camara)
        timezone = 'T10:00:00.03Z'

        self.tweet = {
            "id_tweet": 10,
            "id_author": 111111,
            "text": "Tweet freixo",
            "data_criado": datetime.strptime(f'2022-05-03{timezone}', Setup().ISO_FORMAT),
            "likes": 10,
            "retweets": 10,
            "respostas": 10

        }

    def test_recupera_parlmanetares_casa(self):
        """
        Testa a funcao recupera_parlmanetares_casa
        """
        self.assertEqual(len(self.senadores) + self.CORRIGIR_SENADO, 81)
        self.assertEqual(len(self.deputados), 513)

    def test_procura_parlamentares_sem_perfil(self):
        """
        Testa a funcao procura_parlamentares_sem_perfil
        """
        geral, senado, camara = procura_parlamentares_sem_perfil()
        num_senadores = 81
        num_deputados = 513
        self.assertEqual(geral, num_senadores+num_deputados)
        self.assertEqual(senado, num_senadores)
        self.assertEqual(camara, num_deputados)

        novo_senador = ParlamentarPerfil(
            entidade=self.senadores[0], twitter_id=123, is_personalidade=False, name='teste')
        novo_senador.save()

        novo_deputado = ParlamentarPerfil(
            entidade=self.deputados[0], twitter_id=123, is_personalidade=False, name='teste')
        novo_deputado.save()

        geral, senado, camara = procura_parlamentares_sem_perfil()

        self.assertEqual(senado, num_senadores - 1)
        self.assertEqual(camara, num_deputados - 1)
        self.assertEqual(geral, num_senadores+num_deputados - 2)

    def test_get_tweets_info(self):
        """
        Testa o disparo do signal ao criar um tweet e
        a atualização ao criar outro
        """
        twitter_id = '40053694'

        primeiro_tweet = Setup().create_tweet(**self.tweet)  # cria tweet e dispara signal
        primeiro_tweets_info = TweetsInfo().processa_atual_info()
        self.assertEqual(primeiro_tweet.id,
                         primeiro_tweets_info.tweet_mais_novo_id)

        self.assertEqual(primeiro_tweet.id,
                         primeiro_tweets_info.tweet_mais_antigo_id)

        self.assertEqual(primeiro_tweets_info.numero_total_tweets, 1)
        self.assertEqual(primeiro_tweets_info.numero_parlamentares_sem_perfil,
                         513+81)

        segundo_tweet = Setup().create_tweet(**self.tweet)  # cria tweet e dispara signal
        segundo_tweets_info = TweetsInfo().processa_atual_info()
        self.assertEqual(segundo_tweets_info.tweet_mais_novo_id,
                         segundo_tweet.id)
        self.assertEqual(segundo_tweets_info.tweet_mais_antigo_id,
                         primeiro_tweet.id)
        self.assertEqual(segundo_tweets_info.numero_total_tweets, 2)
        self.assertEqual(segundo_tweets_info.numero_parlamentares_sem_perfil, 513+81)

    def test_del_tweet_meio(self):
        """
        Testa a deleção de tweets que não são os registrados na model TweetsInfo

        """
        primeiro_tweet = Setup().create_tweet(**self.tweet)
        segundo_tweet = Setup().create_tweet(**self.tweet)
        terceiro_tweet = Setup().create_tweet(**self.tweet)

        tweets_info = TweetsInfo().processa_atual_info()
        self.assertEqual(primeiro_tweet.id, tweets_info.tweet_mais_antigo_id)
        self.assertEqual(terceiro_tweet.id, tweets_info.tweet_mais_novo_id)
        self.assertEqual(tweets_info.numero_total_tweets, 3)

        segundo_tweet.delete()
        tweets_info = TweetsInfo().processa_atual_info()
        self.assertEqual(primeiro_tweet.id, tweets_info.tweet_mais_antigo_id)
        self.assertEqual(terceiro_tweet.id, tweets_info.tweet_mais_novo_id)
        self.assertEqual(tweets_info.numero_total_tweets, 2)

    def test_del_tweet_extremo(self):
        primeiro_tweet = Setup().create_tweet(**self.tweet)
        segundo_tweet = Setup().create_tweet(**self.tweet)
        terceiro_tweet = Setup().create_tweet(**self.tweet)
        # del tweet mais antigo
        primeiro_tweet.delete()
        tweets_info = TweetsInfo().processa_atual_info()
        self.assertEqual(tweets_info.numero_total_tweets, 2)
        self.assertEqual(segundo_tweet.id, tweets_info.tweet_mais_antigo_id)
        self.assertEqual(terceiro_tweet.id, tweets_info.tweet_mais_novo_id)
        # del tweet mais novo
        quarto_tweet = Setup().create_tweet(**self.tweet)
        quarto_tweet.delete()
        tweets_info = TweetsInfo().processa_atual_info()
        self.assertEqual(tweets_info.numero_total_tweets, 2)
        self.assertEqual(segundo_tweet.id, tweets_info.tweet_mais_antigo_id)
        self.assertEqual(terceiro_tweet.id, tweets_info.tweet_mais_novo_id)

    def test_del_parlamentar(self):
        Setup().create_tweet(**self.tweet)
        Setup().create_tweet(**self.tweet)
        Setup().create_tweet(**self.tweet)

        novo_senador = ParlamentarPerfil(
            entidade=self.senadores[0], twitter_id=123, is_personalidade=False, name='teste')
        novo_senador.save()

        novo_deputado = ParlamentarPerfil(
            entidade=self.deputados[0], twitter_id=123, is_personalidade=False, name='teste')
        novo_deputado.save()

        geral, senado, camara = procura_parlamentares_sem_perfil()

        num_senadores = 81
        num_deputados = 513
        self.assertEqual(senado, num_senadores - 1)
        self.assertEqual(camara, num_deputados - 1)
        self.assertEqual(geral, num_senadores+num_deputados - 2)

        novo_deputado.delete()
        geral, senado, camara = procura_parlamentares_sem_perfil()
        self.assertEqual(camara, num_deputados)
        self.assertEqual(geral, num_senadores+num_deputados - 1)

        novo_senador.delete()
        geral, senado, camara = procura_parlamentares_sem_perfil()
        self.assertEqual(senado, num_senadores)
        self.assertEqual(geral, num_senadores+num_deputados)
