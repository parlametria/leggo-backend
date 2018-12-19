from rest_framework.test import APITestCase
from api.utils import import_all_data


class InfoTests(APITestCase):
    def test_info(self):
        '''
        Check info
        '''
        url = '/info/'
        response = self.client.get(url)
        self.assertTrue(response.data['last_update_trams'])


class ProposicaoTests(APITestCase):

    def setUp(self):
        import_all_data()

    def test_list(self):
        '''
        Check proposicao list
        '''
        url = '/proposicoes/'
        response = self.client.get(url)
        self.assertGreater(len(response.data), 0)

    def test_detail(self):
        '''
        Check proposicao detail
        '''
        url = '/proposicoes/camara/2120775'
        response = self.client.get(url)
        self.assertEqual(response.data['data_apresentacao'], '2016-12-13')
