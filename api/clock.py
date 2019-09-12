from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=15, minute=30)
def scheduled_job():
    print('This job is run every weekday at 3:20pm.')

sched.start()
