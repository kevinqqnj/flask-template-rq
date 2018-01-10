# encoding: utf-8
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify, g
import redis
from rq import push_connection, pop_connection, Queue
from rq.job import Job
from . import main
from . import tasks

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
        response = {'status': 'unknown'}
    else:
        response = {
            'status': job.get_status(),
            'result': job.result,
        }
        if job.is_failed:
            response['message'] = job.exc_info.strip().split('\n')[-1]
    return jsonify(response)


@main.route('/_run_task', methods=['POST'])
def run_task():
    task = request.form.get('task')
    q = Queue()
    job = q.enqueue(tasks.run, task)
    return jsonify({}), 202, {'Location': url_for('main.job_status', job_id=job.get_id())}
