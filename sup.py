#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: uwsgi, better headers maybe

import sys

from os import chmod, environ, path
from yaml import safe_load
from uuid import uuid4
from pprint import pprint
from datetime import datetime
from subprocess import run, CalledProcessError
from logging.config import dictConfig

from werkzeug.utils import secure_filename
from flask import (Blueprint, Flask,
    render_template, request, send_from_directory)


UPLOAD_DIR = '/data'
CONFIG_DIR = '/sup'

DEFAULT_INTRO = 'Please start the file upload by first selecting file.'

PREFIX = environ.get('URL_PREFIX', '/')
blueprint = Blueprint('sup', __name__, template_folder='tmpl')
dictConfig({
    'version': 1,
    'root': { 'level': 'INFO' }
})


def get_value(c, d, i, j):
    try:
        return c.get(i).get(j, d)
    except AttributeError:
        return d


def get_config():
    conffile = path.join(CONFIG_DIR, 'config.yaml')
    with open(conffile) as File:
        cnf = safe_load(File)
        return {
            'udir': UPLOAD_DIR,
            'addr': get_value(cnf, '0.0.0.0', 'bind', 'addr'),
            'port': get_value(cnf, '8000', 'bind', 'port'),
            'exts': get_value(cnf, None, 'security', 'allowed_extensions'),
            'udfn': get_value(cnf, False, 'security', 'allow_user_filenames'),
            'size': 1024*1024*int(get_value(cnf, 1, 'security', 'max_upload_size')),
            'title': get_value(cnf, 'Sup', 'ui', 'title'),
            'intro': get_value(cnf, DEFAULT_INTRO, 'ui', 'intro'),
            'hooks': cnf.get('hooks') or [] }


def is_allowed(filename):
    if app.config['exts']:
        if filename and filename.rsplit('.')[-1] in app.config['exts']:
            return 200
        else:
            return 403
    return 200


def decide_fn(filename):
    if filename and app.config['udfn']:
        return secure_filename(filename)
    ts = datetime.now().strftime('%F-%H-%M-%S')
    return '{}.{}.bin'.format(ts, str(uuid4())[24:])


def run_hook(hook, filename):
    script = path.join(CONFIG_DIR, hook)
    if not path.exists(script):
        app.logger.warning('Hook not found: %s', hook)
        return
    cmd = [script, app.config['udir'], filename]
    try:
        run(cmd, check=True, encoding='utf-8')
    except CalledProcessError as cpe:
        return 'Upload hook failed', 500
    except FileNotFoundError as fnfe:
        return 'Upload hook not found', 500
    except PermissionError as pe:
        return 'Upload hook permission failed', 500
    app.logger.info('Ran hook: %s', hook)


def upload_request(req):
    if 'file' not in req.files:
        app.logger.error('400 Missing input')
        return 'Missing input', 400
    f = req.files['file']
    code = is_allowed(f.filename)
    if code != 200:
        return 'Invalid filename', code
    filename = decide_fn(f.filename)
    fullpath = path.join(app.config['udir'], filename)
    f.save(fullpath)
    app.logger.info('Received: %s', filename)
    for hook in app.config['hooks']:
        run_hook(hook, filename)
    return 'OK', 200


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/<filename>', methods=['GET'])
def index(filename=None):
    if request.method == 'POST':
        return upload_request(request)
    elif filename == 'favicon.ico':
        return send_from_directory('static', 'favicon.png')
    elif filename:
        return send_from_directory('static', filename)
    else:
        return render_template('upload.html',
            title=app.config['title'],
            intro=app.config['intro'])


def main():
    debug = bool(environ.get('DEBUG', False))
    app.config.update(get_config())
    if debug:
        pprint(app.config)
    if not path.isdir(app.config['udir']):
        print('Upload directory does not exist', file=sys.stderr)
        sys.exit(1)
    app.run(host=app.config['addr'], port=app.config['port'], debug=debug)


app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix=PREFIX)

if __name__ == '__main__':
    main()
