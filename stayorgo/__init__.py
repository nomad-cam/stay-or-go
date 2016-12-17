from flask import Flask
from flask_bootstrap import Bootstrap,StaticCDN
from flask_caching import Cache
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
StaticCDN(static_endpoint='/static')

cache = Cache(app,config={'CACHE_TYPE': 'filesystem',
                      'CACHE_DEFAULT_TIMEOUT': 300,
                      'CACHE_DIR': BASE_DIR + '/static/cache',
                      'CACHE_THRESHOLD': 5})

Bootstrap(app)

import stayorgo.config
import stayorgo.views