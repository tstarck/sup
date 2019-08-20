#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from os import environ, path
from uuid import uuid4
from pprint import pformat
from datetime import datetime
from subprocess import run, CalledProcessError

from yaml import safe_load
from werkzeug.utils import secure_filename
from flask import (Blueprint, Flask, render_template,
                   request, send_from_directory)


CONFIG_DIR = '/conf'
DEFAULT_INTRO = 'Please start the file upload by first selecting file.'

blueprint = Blueprint('sup', __name__, template_folder='tmpl')


def get_value(conf, section, key, default):
    try:
        return conf.get(section).get(key, default)
    except AttributeError:
        return default


def get_config():
    cnf = {}
    configpath = path.join(CONFIG_DIR, 'config.yaml')
    try:
        with open(configpath) as config:
            cnf = safe_load(config)
    except FileNotFoundError:
        pass
    except NotADirectoryError:
        pass
    max_size = get_value(cnf, 'security', 'max_upload_size', 1024)
    return {
        'DEBUG': bool(environ.get('DEBUG', False)),
        'MAX_CONTENT_LENGTH': 1024*int(max_size),
        'port': get_value(cnf, 'app', 'port', '8000'),
        'prefix': get_value(cnf, 'app', 'url_prefix', '/'),
        'updir': get_value(cnf, 'app', 'upload_dir', '/data'),
        'hooks': get_value(cnf, 'app', 'hooks', []),
        'udfn': get_value(cnf, 'security', 'allow_user_filenames', False),
        'exts': get_value(cnf, 'security', 'allowed_extensions', None),
        'title': get_value(cnf, 'ui', 'title', 'Sup'),
        'intro': get_value(cnf, 'ui', 'intro', DEFAULT_INTRO)}


def is_allowed(filename):
    if not app.config['exts']:
        return 200
    if filename and filename.rsplit('.')[-1] in app.config['exts']:
        return 200
    return 403


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
    cmd = [script, app.config['updir'], filename]
    try:
        run(cmd, check=True, encoding='utf-8')
    except CalledProcessError:
        return 'Upload hook failed', 500
    except FileNotFoundError:
        return 'Upload hook not found', 500
    except PermissionError:
        return 'Upload hook permission failed', 500
    app.logger.info('Ran hook: %s', hook)


def upload_request(req):
    if 'file' not in req.files:
        app.logger.error('400 Missing input')
        return 'Missing input', 400
    fobj = req.files['file']
    code = is_allowed(fobj.filename)
    if code != 200:
        return 'Invalid filename', code
    filename = decide_fn(fobj.filename)
    fobj.save(path.join(app.config['updir'], filename))
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
    return render_template('upload.html',
            title=app.config['title'], intro=app.config['intro'])


def main():
    app.logger.debug(pformat(app.config))
    if not path.isdir(app.config['updir']):
        app.logger.error('Upload directory does not exist')
        sys.exit(1)
    app.run(host='0.0.0.0', port=app.config['port'], debug=app.config['DEBUG'])


app = Flask(__name__)
app.config.update(get_config())
app.register_blueprint(blueprint, url_prefix=app.config['prefix'])

if __name__ == '__main__':
    main()
