from django.db.models.signals import post_save
from django.dispatch import receiver

from api.model.proposicao import Proposicao
from usuario.models import UsuarioProposicao


@receiver(post_save, sender=Proposicao, dispatch_uid="get_tweets_ref")
def get_tweets(sender,  instance, created, **kwargs):
    if (created):
        from requests import post, get
        import json
        import traceback
        from dotenv import dotenv_values

        AIRFLOW_HOST = dotenv_values(f"./.ENV").get('AIRFLOW_HOST')

        AIRFLOW_CREDENTIALS = dotenv_values(f"./.ENV").get('AIRFLOW_CREDENTIALS')

        PATH = 'api/v1/dags'
        DAG_ID = 'process_new_tweets'

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {AIRFLOW_CREDENTIALS}"
        }
        conf = instance.__dict__
        if(conf.get('_state', False)):
            conf.pop('_state')

        body = {
            "dag_run_id": f"{instance.id_leggo}",  # unique or 409
            "conf": {
                **conf,

            }
        }

        try:
            response = post(f"{AIRFLOW_HOST}/{PATH}/{DAG_ID}/dagRuns",
                            headers=headers, json=body)
            # print(json.loads(response.content))
            return instance, response
        except Exception as e:
            # print(traceback.format_exc())
            print(e)
            return instance, response


@receiver(post_save, sender=Proposicao, dispatch_uid="update_user_ref")
def update_user(sender, instance, **kwargs):
    encontrouProposicao = UsuarioProposicao.objects.filter(proposicao=instance.id_leggo)
    if not encontrouProposicao:
        up = UsuarioProposicao()
        up.proposicao = instance.id_leggo
        up.save()
        return up
    else:
        print(encontrouProposicao[0].usuarios.all())
        return encontrouProposicao[0].usuarios.all()
