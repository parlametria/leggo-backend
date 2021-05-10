from django.core.management.base import BaseCommand

from api.management.commands.clear_and_import import (
    get_models,
    atualiza_atores,
    atualiza_comissoes,
    atualiza_emendas,
    atualiza_etapa_proposicao,
    atualiza_pauta,
    atualiza_pressao,
    atualiza_progresso,
    atualiza_proposicoes,
    atualiza_temperatura,
    atualiza_tramitacoes,
    atualiza_coautoria_node,
    atualiza_coautoria_edge,
    atualiza_autorias,
    atualiza_interesse,
    atualiza_entidades,
    atualiza_autores_proposicoes,
    atualiza_relatores_proposicoes,
    atualiza_destaque,
    atualiza_governismo,
    atualiza_disciplina,
    atualiza_votacoes_sumarizadas,
    atualiza_locais_atuais,
    atualiza_proposicoes_apensadas
)


class Command(BaseCommand):
    help = 'Importa dados'

    def add_arguments(self, parser):
        parser.add_argument('--model')
        parser.add_argument('--list', action='store_true')

    def handle(self, *args, **options):
        models = get_models()
        if options['model']:
            model = options['model'].lower()

            if model == 'list_models':
                s = '\n'.join(models)
                print('Models disponíveis para atualização: \n')
                print(s)
                exit(0)

            elif model not in models:
                print('Model não encontrado.')
                exit(1)

            else:
                if model == "ator":
                    atualiza_atores()

                elif model == "comissao":
                    atualiza_comissoes()

                elif model == "emenda":
                    atualiza_emendas()

                elif model == "etapa_proposicao":
                    atualiza_etapa_proposicao()

                elif model == "pauta_historico":
                    atualiza_pauta()

                elif model == "pressao":
                    atualiza_pressao()

                elif model == "progresso":
                    atualiza_progresso()

                elif model == "proposicao":
                    atualiza_proposicoes()

                elif model == "temperatura_historico":
                    atualiza_temperatura()

                elif model == "tramitacao_event":
                    atualiza_tramitacoes()

                elif model == "coautoria_node":
                    atualiza_coautoria_node()

                elif model == "coautoria_edge":
                    atualiza_coautoria_edge()

                elif model == "autoria":
                    atualiza_autorias()

                elif model == "interesse":
                    atualiza_interesse()

                elif model == "entidade":
                    atualiza_entidades()

                elif model == "autores_proposicao":
                    atualiza_autores_proposicoes()

                elif model == "relatores_proposicao":
                    atualiza_relatores_proposicoes()

                elif model == "destaques":
                    atualiza_destaque()

                elif model == "governismo":
                    atualiza_governismo()

                elif model == "disciplina":
                    atualiza_disciplina()

                elif model == "votacoes_sumarizadas":
                    atualiza_votacoes_sumarizadas()

                elif model == "local_atual_proposicao":
                    atualiza_locais_atuais()

                elif model == "proposicao_apensada":
                    atualiza_proposicoes_apensadas()
