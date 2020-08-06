from rest_framework.test import APITestCase
from api.model.emenda import Emendas
from api.model.etapa_proposicao import EtapaProposicao
from api.model.proposicao import Proposicao
from api.model.temperatura_historico import TemperaturaHistorico
from api.model.interesse import Interesse
import json


class ProposicaoTests(APITestCase):

    def setUp(self):
        create_proposicao(self)
        self.url = '/proposicoes/'

    def test_list(self):
        '''
        Check proposicao list
        '''
        response = self.client.get(self.url)
        self.assertGreater(len(response.data), 0)

    def test_etapa_proposicao(self):
        '''
        Check proposicao detail
        '''
        url_detail = (self.url + str(self.proposicao.id_leggo))
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class EmendasTest(APITestCase):

    def setUp(self):
        create_proposicao(self)
        self.emenda = Emendas(
            data_apresentacao='2004-06-08',
            distancia=2.5,
            codigo_emenda=10,
            inteiro_teor="",
            numero=1,
            local='CCJ',
            autor="Joao",
            proposicao=self.etapa_proposicao
        )

        self.emenda.save()
        self.url = ('/emenda/' + self.etapa_proposicao.casa + '/' +
                    self.etapa_proposicao.id_ext)

    def test_emendas_list(self):
        '''
        Check emendas list
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)


def create_proposicao(self):
    '''
    Create a proposicao and an etapa_proposicao object and save on test database
    '''
    etapa_proposicao = EtapaProposicao(
        id_leggo=1,
        id_ext='257161',
        casa='camara',
        data_apresentacao='2004-06-08',
        sigla_tipo='PL',
        numero='3729',
        regime_tramitacao='Urgência',
        forma_apreciacao='Plenário',
        ementa='Dispõe sobre o licenciamento ambiental...',
        justificativa='',
        autor_nome='Luciano Zica PSOL/CE',
        relator_id=74050,
        relator_id_parlametria=74050,
        em_pauta=False
    )
    etapa_proposicao.save()

    proposicao = Proposicao(id_leggo=1)
    proposicao.save()
    proposicao.etapas.set([etapa_proposicao])
    proposicao.save()

    interesse = Interesse(
        id_leggo=1,
        interesse='leggo',
        apelido='Lei do Licenciamento Ambiental',
        tema='Meio Ambiente',
        tema_slug='meio-ambiente',
        proposicao=proposicao
    )
    interesse.save()

    temperatura = TemperaturaHistorico(
        temperatura_periodo=1.25,
        temperatura_recente=1.67,
        periodo='2018-06-08',
        proposicao=proposicao
    )

    temperatura2 = TemperaturaHistorico(
        temperatura_periodo=0,
        temperatura_recente=1.37,
        periodo='2018-06-15',
        proposicao=proposicao
    )

    temperatura.save()
    temperatura2.save()

    self.proposicao = proposicao
    self.etapa_proposicao = etapa_proposicao


def create_temperatura(self, proposicao):
    '''
    Create a temperatura object and save on test database
    '''
    temperatura = TemperaturaHistorico(
        temperatura_periodo=1.25,
        temperatura_recente=1.25,
        periodo='2018-06-08',
        proposicao=proposicao
    )

    temperatura.save()

    self.temperatura = temperatura


class TemperaturaTests(APITestCase):
    def setUp(self):
        create_proposicao(self)
        self.url = '/temperatura/max/'

    def test_temperatura_max(self):
        '''
        Check maximum temperature value
        '''
        response = self.client.get(self.url)
        res = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['max_temperatura_periodo'], 1.67)

    def test_invalid_date(self):
        '''
        Check invalid date
        '''
        response = self.client.get(self.url + '?data_inicio=2020-01-50')

        self.assertEqual(response.status_code, 400)

    def test_invalid_final_date(self):
        '''
        Check invalid date
        '''
        response = self.client.get(self.url + '?data_fim=2020-01-500')

        # Usa a data atual como default em caso de erro com a data de parâmetro
        self.assertEqual(response.status_code, 200)

    def test_init_date(self):
        '''
        Check invalid date
        '''
        response = self.client.get(self.url + '?data_inicio=2018-06-08')
        res = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['max_temperatura_periodo'], 1.67)
