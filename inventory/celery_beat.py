from celery.schedules import crontab

from .celery_app import app

app.conf.beat_schedule = {
    'run-sample-task': {
        'task': 'sample_task',
        'schedule': crontab(minute='*/5'),
        'args': (3, 7),
    },
}
app.conf.timezone = 'UTC'
