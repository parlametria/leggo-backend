from django.core.management.base import BaseCommand
from ...model.anotacao import Anotacao


class Command(BaseCommand):
    def handle(self, *args, **options):
        Anotacao.objects.all().delete()
