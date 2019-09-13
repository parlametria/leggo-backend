from apscheduler.schedulers.blocking import BlockingScheduler
from django.core import management
from django.core.management.commands import flush, import_data_from_remote


sched = BlockingScheduler()
print('Iniciando scheduler...')

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    try:
        management.call_command(flush.Command(), verbosity=3)
        mangement.call_command(import_data_from_remote.Command(), verbosity=3)
    except Exception as e:
        print(e)

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17, minute=22)
#def scheduled_job():
#    print('This job is run every weekday at 5:20pm.')

sched.start()
