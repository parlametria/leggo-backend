from rest_framework.test import APITestCase


class ProposicaoTests(APITestCase):
    def test_list(self):
        """
        Check list
        """
        url = '/proposicoes/'
        response = self.client.get(url)
        self.assertEqual(response.data[1], 'boa tarde')
