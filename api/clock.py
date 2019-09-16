from apscheduler.schedulers.blocking import BlockingScheduler
from django.core import management
from agorapi import settings

management.setup_environ(settings)

sched = BlockingScheduler()
print('Iniciando scheduler...')

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    try:
        management.call_command('flush', '--no-input')
        mangement.call_command('import_data_from_remote', verbosity=3)
    except Exception as e:
        print(e)

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17, minute=22)
#def scheduled_job():
#    print('This job is run every weekday at 5:20pm.')

sched.start()
