# encoding: utf-8
from flask import Flask, abort, redirect, url_for, request
from config import config
from flask_redis import FlaskRedis
from flask_cache import Cache
import time
from urllib import parse

cache = Cache()
r = FlaskRedis()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  parse.uses_netloc.append("redis")
  redis_url = parse.urlparse(app.config['REDISTOGO_URL'])
  cache.init_app(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fcache',
    'CACHE_REDIS_HOST': redis_url.hostname,
    'CACHE_REDIS_PORT': redis_url.port,
    'CACHE_REDIS_USERNAME': redis_url.username or '',
    'CACHE_REDIS_PASSWORD': redis_url.password or '',
    })
  r.init_app(app)

  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app
