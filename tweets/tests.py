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


class PerfilTests(TestCase):
    def setUp(self):
        create_entidades()

    def test_populate(self):
        perfil = Perfil()
        perfil.populate_parlamentar()
        self.assertTrue(Perfil.objects.get(entidade_id=1886))
        self.assertTrue(Perfil.objects.get(entidade_id=4155))


class PressaoTests(TestCase):
    def setUp(self):
        create_perfils()
        create_proposicao(self)
        create_tweets()

    def test_pressao(self):
        end_time = '2022-05-05T15:42:15.000Z'
        pro = Proposicao.objects.get(id_leggo=1)
        convert_date = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        pressao = Pressao()
        pressao.proposicao = pro
        pressao.data_consulta = convert_date
        pressao.save()

        self.assertEqual(pressao.total_likes, 70)
        self.assertEqual(pressao.total_engajamento, 345)
        self.assertEqual(pressao.total_usuarios, 2)
        self.assertEqual(pressao.total_tweets, 10)
        test_tweets_range(self, end_time, '2022-05-03', pressao.get_tweets())


class EngajamentoTests(TestCase):
    def setUp(self):
        create_perfils()
        create_proposicao(self)
        create_tweets()

    def test_engajamento(self):
        end_time = '2022-05-05T15:42:15.000Z'
        id_author = 45870897
        perfil = Perfil.objects.get(twitter_id=id_author)
        convert_date = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        engajamento = Engajamento()
        engajamento.perfil = perfil
        engajamento.data_consulta = convert_date
        engajamento.proposicao = Proposicao.objects.get(id_leggo=1)
        engajamento.save()
        self.assertEqual(engajamento.total_engajamento, 120)
        test_tweets_range(self, end_time, '2022-05-03', engajamento.get_tweets())


class ProposicaoSignalTests(TestCase):
    def setUp(self):
        User.objects.create(username="u1")
        User.objects.create(username="u2")
        User.objects.create(username="u3")

    def test_signal_on_create_model(self):
        pid = 1
        proposicao = Proposicao(id_leggo=pid)

        self.assertFalse(UsuarioProposicao.objects.filter(proposicao=pid))

        proposicao.save()

        self.assertTrue(UsuarioProposicao.objects.filter(proposicao=pid))

    def test_signal_function_return(self):
        pid = 1
        proposicao = Proposicao()
        proposicao.id_leggo = pid

        call_create_usuario_proposicao = signals.update_user(  # noqa
            Proposicao, proposicao
        )
        proposicao_usuario = UsuarioProposicao.objects.get(proposicao=pid)

        self.assertTrue(proposicao_usuario)

        proposicao_usuario.usuarios.add(
            User.objects.all()[0], User.objects.all()[1], User.objects.all()[2]
        )

        call_list_usuario_proposicao_usuarios = signals.update_user(
            Proposicao, proposicao
        )

        self.assertTrue(call_list_usuario_proposicao_usuarios.count() == 3)


def create_entidades():
    bolsonaro = Entidade(
        id=1886,
        legislatura=53,
        id_entidade=74847,
        id_entidade_parlametria=174847,
        casa='camara',
        nome='Jair Bolsonaro',
        sexo='M',
        partido='PSL',
        uf='RJ',
        situacao='Titular',
        em_exercicio=0,
        is_parlamentar=1
    )
    bolsonaro.save()

    freixo = Entidade(
        id=4155,
        legislatura=56,
        id_entidade=76874,
        id_entidade_parlametria=176874,
        casa='camara',
        nome='Marcelo Freixo',
        sexo='M',
        partido='PSOL',
        uf='RJ',
        situacao='Titular',
        em_exercicio=1,
        is_parlamentar=1
    )
    freixo.save()


def create_perfils():
    from django.db import models

    # make sure they already exists
    create_entidades()

    bolsonaro = Entidade.objects.get(id=1886)
    freixo = Entidade.objects.get(id=4155)

    pFreixo = Perfil(entidade=freixo, twitter_id=45870897,
                     is_personalidade=False, name="Marcelo Freixo")
    pFreixo.save()

    pBolsonaro = Perfil(entidade=bolsonaro, twitter_id=128372940,
                        is_personalidade=False, name="Jair M. Bolsonaro")
    pBolsonaro.save()


def create_proposicao(self):
    """
    Create a proposicao and an etapa_proposicao object and save on test database
    """
    etapa_proposicao = EtapaProposicao(
        id_leggo="1",
        id_ext="257161",
        casa="camara",
        data_apresentacao="2004-06-08",
        sigla_tipo="PL",
        numero="3729",
        regime_tramitacao="Urgência",
        forma_apreciacao="Plenário",
        ementa="Dispõe sobre o licenciamento ambiental...",
        justificativa="",
        relator_id=74050,
        relator_id_parlametria=174050,
        em_pauta=False,
    )
    etapa_proposicao.save()

    proposicao = Proposicao(id_leggo=1)
    proposicao.save()
    proposicao.etapas.set([etapa_proposicao])
    proposicao.save()

    interesse = Interesse(
        id_leggo="1",
        interesse="leggo",
        apelido="Lei do Licenciamento Ambiental",
        tema="Meio Ambiente",
        tema_slug="meio-ambiente",
        proposicao=proposicao,
    )
    interesse.save()

    self.proposicao = proposicao
    self.etapa_proposicao = etapa_proposicao


def create_tweets():
    proposicao = Proposicao.objects.get(id_leggo=1)
    id_author = 45870897
    perfil = Perfil.objects.get(twitter_id=id_author)

    date_end = datetime.strptime('2022-05-05', '%Y-%m-%d')
    date_end_menos1 = datetime.strptime('2022-05-05', '%Y-%m-%d') - timedelta(days=1)
    date_end_menos2 = datetime.strptime('2022-05-05', '%Y-%m-%d') - timedelta(days=2)

    date_out_menos1d = date_end_menos2 - timedelta(days=1)
    date_out_mais1d = date_end + timedelta(days=1)
    date_out_maisano = date_end + timedelta(days=365)
    date_out_menosano = date_end - timedelta(days=365)
    date_out_maismes = date_end + timedelta(days=30)
    date_out_menosmes = date_end - timedelta(days=30)

    dates_on_range = [date_end, date_end_menos1, date_end_menos2, date_end_menos2,
                      date_end_menos1, date_end, date_end, date_end_menos1, date_end_menos2, date_end_menos2]
    dates_out_range = [date_out_menos1d, date_out_menosmes, date_out_menosano, date_out_mais1d, date_out_maisano,
                       date_out_maismes, date_out_menos1d, date_out_menosmes, date_out_menosano, date_out_mais1d]

    for i in range(10):
        if i % 2 == 0:
            new_tweet = Tweet(
                id_tweet=i,
                id_author=id_author,  # freixo
                text="Tweet freixo",
                data_criado=dates_on_range.pop(),
                likes=i,
                retweets=2 * i,
                respostas=3 * i
            )
            new_tweet.save()
            new_tweet.proposicao.add(proposicao)

            wrong_tweet = Tweet(
                id_tweet=i + 1000,
                id_author=id_author,  # freixo
                text="Tweet freixo",
                data_criado=dates_out_range.pop(),
                likes=i,
                retweets=2 * i,
                respostas=3 * i
            )
            wrong_tweet.save()
            wrong_tweet.proposicao.add(proposicao)

            new_tweet.author = perfil
            new_tweet.save()

            wrong_tweet.author = perfil
            wrong_tweet.save()

        else:
            new_tweet = Tweet(
                id_tweet=i + 10000,
                id_author=111111,  # freixo
                text="Tweet outro",
                data_criado=dates_on_range.pop(),
                likes=2 * i,
                retweets=3 * i,
                respostas=4 * i
            )
            new_tweet.save()
            new_tweet.proposicao.add(proposicao)

            wrong_tweet = Tweet(
                id_tweet=i + 100,
                id_author=111111,  # freixo
                text="Tweet outro",
                data_criado=dates_out_range.pop(),
                likes=2 * i,
                retweets=3 * i,
                respostas=4 * i
            )
            wrong_tweet.save()
            wrong_tweet.proposicao.add(proposicao)


def test_tweets_range(self, end, start, tweets):
    ISO_DATA = '%Y-%m-%dT%H:%M:%S.%f%z'
    DATA = '%Y-%m-%d'
    DATE_SIZE = 10
    c_end = datetime.strptime(end[:DATE_SIZE], DATA)
    c_start = datetime.strptime(start[:DATE_SIZE], DATA)

    self.assertIsNotNone(tweets)

    for tweet in tweets:

        self.assertFalse(datetime.strptime(str(tweet.data_criado), DATA) > c_end)
        self.assertFalse(datetime.strptime(str(tweet.data_criado), DATA) < c_start)
