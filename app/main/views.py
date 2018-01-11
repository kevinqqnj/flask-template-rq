# encoding: utf-8
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify, g
import redis
from rq import push_connection, pop_connection, Queue
from rq.job import Job
from . import main
from . import tasks
from .. import r

@main.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

def get_redis_connection():
    redis_connection = getattr(g, '_redis_connection', None)
    if redis_connection is None:
        redis_url = current_app.config['REDISTOGO_URL']
        redis_connection = g._redis_connection = redis.from_url(redis_url)
    return redis_connection

@main.before_request
def push_rq_connection():
    push_connection(get_redis_connection())

@main.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()

@main.route('/status/<job_id>')
def job_status(job_id):
    q = Queue()
    job = q.fetch_job(job_id)
    if job is None:
        # job ttl expired or job_id wrong
        rsp = {
	    	'result': 'not found',
	    	'job': {}
	   }
    else:
	    rsp = {
	    	'result': 'success',
	    	'job': {
	    		'name': r.hget('task:%s'%job_id, 'name').decode('ascii'),
	            'job_id': job_id,
	            'status': job.get_status(),
	            'result': job.exc_info.strip().split('\n')[-1] if  job.is_failed else job.result,
	            'start_time': job.__dict__['started_at'],
	            'finish_time': job.__dict__['ended_at'],
	    	}
	    }
    return jsonify(rsp)

@main.route('/_run_task', methods=['POST'])
def run_task():
    jsondata = request.get_json()
    task = jsondata.get('task')
    q = Queue()
    # push to async queue, result cache 3600s.
    job = q.enqueue_call(func=tasks.run, args=(task,), timeout=30, result_ttl=3600)
    print('start queue: tasks...', job.get_id())
    job_id = job.get_id()
    r.sadd('tasks:', job_id)
    r.hmset('task:%s'%job_id, {
    	'status': job.get_status(),
    	'name': task
    })
    rsp = {
    	'result': 'success',
    	'job': {
    		'name': task,
            'job_id': job_id,
            'status': job.get_status(),
            'result': job.result,
            'start_time': job.__dict__['started_at'],
            'finish_time': job.__dict__['ended_at'],
    	}
    }
    return jsonify(rsp), 202, {'Location': url_for('main.job_status', job_id=job_id)}

@main.route('/reset')
def job_reset():
    q = Queue()
    for job in q.jobs:
      	job.cancel()
    r.flushall()
    return jsonify('success')
