from rest_framework.test import APITestCase


class InfoTests(APITestCase):
    def test_info(self):
        '''
        Check info
        '''
        url = '/info/'
        response = self.client.get(url)
        self.assertEqual(response.data['status'], 'ok')


class ProposicaoTests(APITestCase):
    def test_list(self):
        '''
        Check proposicao list
        '''
        url = '/proposicoes/'
        response = self.client.get(url)
        self.assertIsInstance(response.data[1]['ano'], int)
