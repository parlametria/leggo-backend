from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
print('Iniciando scheduler...')

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    try:
        print('This job is run every one minute.')
    except Exception as e:
        print(e)

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17, minute=22)
#def scheduled_job():
#    print('This job is run every weekday at 5:20pm.')

sched.start()
