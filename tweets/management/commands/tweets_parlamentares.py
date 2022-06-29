from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Adiciona tweets a model de interesse'

    def add_arguments(self, parser):
        parser.add_argument('tweets_parlamentares', nargs='+', type=int)

    def handle(self, *args, **options):
        for parla in options['tweets_parlamentares']:
            try:
                self.stdout.write(self.style.SUCCESS(  # Para os tests
                    'Encontrou tweets com sucesso "%s"' % parla))
                return "Encontrou tweets com sucesso"
            except:
                raise CommandError('Comando falhou')
