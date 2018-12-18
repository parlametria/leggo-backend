from rest_framework.test import APITestCase
from api.models import (
    EtapaProposicao, TemperaturaHistorico, Proposicao, Emendas)


class InfoTests(APITestCase):

    def setUp(self):
        import_all_data()

    def test_info(self):
        '''
        Check info
        '''
        url = '/info/'
        response = self.client.get(url)
        self.assertTrue(response.data['last_update_trams'])


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
        url_detail = (self.url + self.etapa_proposicao.casa + '/' +
                      self.etapa_proposicao.id_ext)

        response = self.client.get(url_detail)

        self.assertEqual(response.data['data_apresentacao'],
                         self.etapa_proposicao.data_apresentacao)
        self.assertEqual(response.data['casa'], self.etapa_proposicao.casa)


class TemperaturaHistoricoTest(APITestCase):

    def setUp(self):
        create_proposicao(self)
        create_temperatura(self, self.etapa_proposicao)
        self.url = ('/temperatura/' + self.etapa_proposicao.casa + '/' +
                    self.etapa_proposicao.id_ext)

    def test_get_temperatura(self):
        '''
        Check temperature list from a proposicao
        '''

        response = self.client.get(self.url)

        self.assertTrue('coeficiente' in response.data)
        self.assertTrue('temperaturas' in response.data)

    def test_get_temperatura_detail(self):
        '''
        Check if can get temperature with query params of referenced date
        '''

        url_detail = (self.url +
                      '?semanas_anteriores=12&data_referencia=2018-11-07')
        response = self.client.get(url_detail)

        self.assertEquals(response.data['coeficiente'], 0)
        self.assertTrue('temperaturas' in response.data)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)


class EmendasTest(APITestCase):

    def setUp(self):
        create_proposicao(self)
        self.emenda = Emendas(
            data_apresentacao='2004-06-08',
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
        id_ext='257161',
        casa='camara',
        data_apresentacao='2004-06-08',
        sigla_tipo='PL',
        numero='3729',
        regime_tramitacao='Urgência',
        forma_apreciacao='Plenário',
        ementa='Dispõe sobre o licenciamento ambiental...',
        justificativa='',
        temperatura=5.7,
        autor_nome='Luciano Zica PSOL/CE',
        relator_nome='Dep. Maurício Quintella Lessa (PR-AL)',
        em_pauta=False,
        apelido='Lei do Licenciamento Ambiental',
        tema='Meio Ambiente/Clima'
    )
    etapa_proposicao.save()

    proposicao = Proposicao(
                    apelido='Lei do Licenciamento Ambiental',
                    tema='Meio Ambiente/Clima'
                )
    proposicao.save()
    proposicao.etapas.set([etapa_proposicao])
    proposicao.save()

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
