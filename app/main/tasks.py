# -*- coding: utf-8 -*-
"""
This module implements the tasks to run.
"""
import random
import time
from flask import current_app
from .. import r

def run(task):
    if 'error' in task:
        time.sleep(1)
        1 / 0
    if task.startswith('Short'):
        seconds = 1
    else:
        seconds = random.randint(2, current_app.config['MAX_TIME_TO_WAIT'])
    time.sleep(seconds)
#    r.hset('task:%s'%job_id, 'status', job.get_status())
    return '{} done in {}s'.format(task, seconds)
