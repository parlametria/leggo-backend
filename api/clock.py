from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17, minute=22)
def scheduled_job():
    print('This job is run every weekday at 5:20pm.')

sched.start()
