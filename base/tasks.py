import time

from celery import shared_task


@shared_task(name='sample_task', bind=True)
def sample_task(self, a, b):
    print('Sample task started running..')
    ans = a * b
    time.sleep(5)
    print(f"Task output {ans};")
    print('Sample task ended.')
