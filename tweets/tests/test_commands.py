from io import StringIO
from optparse import make_option
from django.core.management import call_command
from django.test import TestCase
from tweets.tests.test_models import Setup


class TweetsParlamentares(TestCase):
    def setUp(self):
        setup = Setup()
        setup.create_entidades()
        setup.create_perfils()
        prop_1 = '3'
        prop_2 = '4'
        setup.create_tweets_diferente_interesses(prop_1, prop_2)

    def test_command_output(self):
        out = StringIO()
        call_command('tweets_parlamentares', Setup().get_perfil().entidade.id, stdout=out)
        self.assertIn('Encontrou tweets', out.getvalue())
