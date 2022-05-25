import json
from dotenv import dotenv_values
from tweets.models import Proposicao
from .setup import Setup
from django.test import TestCase
from api.signals import get_tweets
import uuid
import traceback


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
