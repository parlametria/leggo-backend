from tweets.models import EngajamentoProposicao, ParlamentarPerfil, Pressao, Tweet
from api.model.proposicao import Proposicao
from api.model.etapa_proposicao import EtapaProposicao
from api.model.interesse import Interesse
from api.model.entidade import Entidade
from datetime import datetime, timedelta
import tweepy
from dotenv import dotenv_values


class Parlamentar:
    def __init__(self, name, twitter_id, entidade_id):
        self.name = name
        self.tid = twitter_id
        self.eid = entidade_id


# python manage.py dumpdata tweets.Tweet - -format json - -indent 2
class Setup:
    @classmethod
    def __init__(self):
        self.end = "2022-05-05"
        self.start = "2022-05-03"
        self.D_FORMAT = "%Y-%m-%d"
        self.ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
        self.D_SIZE = 10
        self.end_c = datetime.strptime(self.end, self.D_FORMAT)
        self.start_c = datetime.strptime(self.start, self.D_FORMAT)

        self.jair = Parlamentar('Jair Bolsonaro', 128372940, 1886)
        self.marcelo = Parlamentar('Marcelo Freixo', 45870897, 4155)
        self.proposicao = 1

    @classmethod
    def geral_setup(self):
        self.create_entidades()
        self.create_perfils()
        self.create_proposicao()
        self.create_tweets()

    @classmethod
    def create_entidades(self):
        bolsonaro = Entidade(
            id=self.jair.eid,
            legislatura=53,
            id_entidade=74847,
            id_entidade_parlametria=174847,
            casa='camara',
            nome=self.jair.name,
            sexo='M',
            partido='PSL',
            uf='RJ',
            situacao='Titular',
            em_exercicio=0,
            is_parlamentar=1
        )
        bolsonaro.save()

        freixo = Entidade(
            id=self.marcelo.eid,
            legislatura=56,
            id_entidade=76874,
            id_entidade_parlametria=176874,
            casa='camara',
            nome=self.marcelo.name,
            sexo='M',
            partido='PSOL',
            uf='RJ',
            situacao='Titular',
            em_exercicio=1,
            is_parlamentar=1
        )
        freixo.save()

    @classmethod
    def create_perfils(self):

        bolsonaro = Entidade.objects.get(id=self.jair.eid)
        freixo = Entidade.objects.get(id=self.marcelo.eid)

        pFreixo = ParlamentarPerfil(entidade=freixo, twitter_id=self.marcelo.tid,
                                    is_personalidade=False, name="Marcelo Freixo")
        pFreixo.save()

        pBolsonaro = ParlamentarPerfil(entidade=bolsonaro, twitter_id=self.jair.tid,
                                       is_personalidade=False, name="Jair M. Bolsonaro")
        pBolsonaro.save()

    @classmethod
    def create_perfil(self, id_entidade_parlametria, twitter_id, name, legislatura=53, **kwargs):
        ent = Entidade(
            id=id_entidade_parlametria,
            legislatura=legislatura,
            id_entidade=74847,
            id_entidade_parlametria=id_entidade_parlametria,
            casa='camara',
            nome=name,
            sexo='M',
            partido='PSL',
            uf='RJ',
            situacao='Titular',
            em_exercicio=0,
            is_parlamentar=1,
            **kwargs
        )
        ent.save()

        # ent = Entidade.objects.get(id_entidade_parlametria=id_entidade_parlametria)
        pp = ParlamentarPerfil(entidade=ent, twitter_id=twitter_id,
                               is_personalidade=False, name=name)
        pp.save()

    @classmethod
    def create_proposicao(self):
        """
        Create a proposicao and an etapa_proposicao object and save on test database
        """
        id_leggo = 1

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
            tema="Meio Ambiente",
            tema_slug="meio-ambiente",
            apelido="Lei do Licenciamento Ambiental",
            proposicao=proposicao,
        )
        interesse.save()
        self.proposicao = proposicao

    @classmethod
    def create_tweet(self, **kwargs):
        new_tweet = Tweet(**kwargs)
        new_tweet.save()
        return new_tweet

    @classmethod
    def create_tweets(self):
        proposicao = Proposicao.objects.get(id_leggo=1)
        perfil = ParlamentarPerfil.objects.get(twitter_id=self.marcelo.tid)

        date_end = self.end_c
        date_end_menos1 = date_end - timedelta(days=1)
        date_end_menos2 = date_end - timedelta(days=2)

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
                    id_author=self.marcelo.tid,
                    text="Tweet freixo",
                    data_criado=dates_on_range.pop(),
                    likes=i,
                    retweets=2 * i,
                    respostas=3 * i
                )
                new_tweet.save()
                new_tweet.proposicao.add(proposicao)
                new_tweet.save()
                new_tweet.author = perfil
                new_tweet.save()

                wrong_tweet = Tweet(
                    id_tweet=i + 1000,
                    id_author=self.marcelo.tid,
                    text="Tweet freixo",
                    data_criado=dates_out_range.pop(),
                    likes=i,
                    retweets=2 * i,
                    respostas=3 * i
                )
                wrong_tweet.save()
                wrong_tweet.proposicao.add(proposicao)
                wrong_tweet.save()
                wrong_tweet.author = perfil
                wrong_tweet.save()

            else:
                new_tweet = Tweet(
                    id_tweet=i + 10000,
                    id_author=111111,
                    text="Tweet outro",
                    data_criado=dates_on_range.pop(),
                    likes=2 * i,
                    retweets=3 * i,
                    respostas=4 * i
                )
                new_tweet.save()
                new_tweet.proposicao.add(proposicao)
                new_tweet.save()

                wrong_tweet = Tweet(
                    id_tweet=i + 100,
                    id_author=111111,
                    text="Tweet outro",
                    data_criado=dates_out_range.pop(),
                    likes=2 * i,
                    retweets=3 * i,
                    respostas=4 * i
                )
                wrong_tweet.save()
                wrong_tweet.proposicao.add(proposicao)
                wrong_tweet.save()

    @classmethod
    def create_tweets_diferente_interesses(self, prop_1, prop_2):
        pro_a = Proposicao(id_leggo=prop_1)
        pro_a.save()
        pro_b = Proposicao(id_leggo=prop_2)
        pro_b.save()
        perfil = ParlamentarPerfil.objects.get(twitter_id=self.marcelo.tid)
        date_end = self.end_c

        interesse_a = Interesse(
            id_leggo=prop_1,
            interesse="_leggo",
            tema="Meio Ambiente",
            tema_slug="meio-ambiente",
            apelido="Lei do Licenciamento Ambiental",
            proposicao=pro_a,
        )
        interesse_a.save()

        diferente = 'outro'
        interesse_b = Interesse(
            id_leggo=prop_2,
            interesse=f"leggo {diferente}",
            tema=f"Meio Ambiente {diferente}",
            tema_slug="meio-ambiente {diferente}",
            apelido="Lei do Licenciamento Ambiental {diferente}",
            proposicao=pro_b,
        )
        interesse_b.save()
        print(pro_a)
        print(pro_b)
        # print(Proposicao.objects.all())

        for i in range(10):
            new_tweet = Tweet(
                id_tweet=i,
                id_author=self.marcelo.tid,
                text="Tweet freixo",
                data_criado=date_end,
                likes=i,
                retweets=2 * i,
                respostas=3 * i
            )
            new_tweet.save()
            # new_tweet.proposicao.add(pro_a if (i % 2) else pro_b)
            if (i % 2):
                new_tweet.proposicao.add(pro_a)
            else:
                new_tweet.proposicao.add(pro_b)
            # new_tweet.proposicao.add(pro_a)
            new_tweet.save()
            new_tweet.author = perfil
            new_tweet.save()

    @classmethod
    def create_pressao(self):
        pressao = Pressao()
        pressao.proposicao = self.get_preposicao()
        pressao.data_consulta = self.end_c
        pressao.save()

    @classmethod
    def create_engajamento(self):
        engajamento = EngajamentoProposicao()
        engajamento.perfil = ParlamentarPerfil.objects.get(twitter_id=self.marcelo.tid)
        engajamento.tid_author = self.marcelo.tid
        engajamento.data_consulta = self.end_c
        engajamento.proposicao = self.get_preposicao()
        engajamento.save()

    @classmethod
    def test_tweets_range(self, tweets):

        for tweet in tweets:
            data = datetime.strptime(
                str(tweet.data_criado), self.D_FORMAT)

            if(data > self.end_c or data < self.start_c):
                return False

        return True

    @classmethod
    def get_preposicao(self):
        id_leggo = 1
        return Proposicao.objects.get(id_leggo=self.proposicao)

    @classmethod
    def get_perfil(self):
        return ParlamentarPerfil.objects.get(twitter_id=self.marcelo.tid)
