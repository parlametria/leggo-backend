from rest_framework.test import APITestCase
from api.model.emenda import Emendas
from api.model.entidade import Entidade
from api.model.etapa_proposicao import EtapaProposicao
from api.model.proposicao import Proposicao
from api.model.temperatura_historico import TemperaturaHistorico
from api.model.interesse import Interesse
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from usuario.models import UsuarioProposicao
import json
from api import signals
from tweets.models import Engajamento, Perfil, Pressao, Proposicao, Tweet
from os import getenv
from dotenv import dotenv_values
import tweepy
from datetime import date, datetime
from functools import reduce


class PerfilTests(TestCase):
  def setUp(self):   
    create_entidades()

  def test_populate(self):
    perfil = Perfil()
    perfil.populate_parlamentar()
    self.assertTrue(Perfil.objects.get(entidade_id=1886))
    self.assertTrue(Perfil.objects.get(entidade_id=4155))

class TweetTests(TransactionTestCase):

  def setUp(self):
    create_perfils()
    create_proposicao(self)

  def test_get(self):
    id = "45870897" #frexo
    search = "Faça como o Baby Yoda e tire seu título. Que a força do voto esteja com você!"
    tweet = Tweet()
    n_results=10
    start_time = '2022-05-03T15:42:15.000Z'
    end_time = '2022-05-05T15:42:15.000Z'    
    req = tweet.get_recent(search, 1, end_time, start_time, n_results=n_results) 

    counter = 0 
    for page in req:
      print(page)
      counter = counter + page.meta.get('result_count')
      
    
    self.assertEqual(counter, n_results)


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
    print(pressao.__dict__)
    print(pressao)

    self.assertTrue(pressao.total_engajamento == 345) 
    self.assertTrue(pressao.total_usuarios == 2) 
    self.assertTrue(pressao.total_tweets == 10) 
            
class EngajamentoTests(TestCase):
  def setUp(self):
    create_perfils()
    create_proposicao(self)
    create_tweets()
  
  def test_pressao(self):
    end_time = '2022-05-05T15:42:15.000Z'    
    id_author = 45870897
    perfil = Perfil.objects.get(twitter_id=id_author) 
    convert_date = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f%z')
    engajamento = Engajamento()
    engajamento.perfil = perfil
    engajamento.data_consulta = convert_date
    engajamento.save()    
    self.assertEqual(engajamento.total_engajamento, 120)

  


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
    legislatura= 53,
    id_entidade= 74847,
    id_entidade_parlametria= 174847,
    casa= 'camara',
    nome= 'Jair Bolsonaro',
    sexo= 'M',
    partido= 'PSL',
    uf= 'RJ',
    situacao= 'Titular',
    em_exercicio= 0,
    is_parlamentar= 1
  )
  bolsonaro.save()

  freixo = Entidade(
    id= 4155,
    legislatura= 56,
    id_entidade= 76874,
    id_entidade_parlametria= 176874,
    casa= 'camara',
    nome= 'Marcelo Freixo',
    sexo= 'M',
    partido= 'PSOL',
    uf= 'RJ',
    situacao= 'Titular',
    em_exercicio= 1,
    is_parlamentar= 1
  )
  freixo.save()

def create_perfils():
  from django.db import models

  #make sure they already exists
  create_entidades()
  
  bolsonaro = Entidade.objects.get(id=1886)
  freixo = Entidade.objects.get(id=4155)

  pFreixo = Perfil(entidade=freixo, twitter_id=45870897, is_personalidade=False, name= "Marcelo Freixo")
  pFreixo.save()

  pBolsonaro = Perfil(entidade=bolsonaro, twitter_id=128372940, is_personalidade=False, name= "Jair M. Bolsonaro")
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

  for i in range(10):
    if i % 2 == 0:
      new_tweet = Tweet(            
        id_tweet = i,
        id_author = id_author, #freixo
        text= "Tweet freixo",
        data_criado = "2022-05-04",
        likes = i,
        retweets = 2 * i, 
        respostas = 3 * i
      )
      new_tweet.save()
      new_tweet.proposicao.add(proposicao)
      perfil = Perfil.objects.get(twitter_id=id_author);
      
      new_tweet.author = perfil
      new_tweet.save()
    else:
      new_tweet = Tweet(            
        id_tweet = i,
        id_author = 111111, #freixo
        text= "Tweet outro",
        data_criado = "2022-05-04",
        likes = 2 * i,
        retweets = 3 * i, 
        respostas = 4 * i
      )
      new_tweet.save()
      new_tweet.proposicao.add(proposicao)
