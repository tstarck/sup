#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: better headers, filename mangle support

import sys

from os import environ, path
from uuid import uuid4
from datetime import datetime

from flask import Blueprint, Flask, render_template, request
from werkzeug.utils import secure_filename


DEF_EXTENSIONS = 'asc bin txt log json yml yaml pdf gif jpg jpeg png gz xz zip'
DEF_INTRO = 'Please start the file upload by first selecting the file.'

blueprint = Blueprint('sup', __name__, template_folder='tmpl')


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return upload_request(request)
    else:
        return render_template('upload.html',
            title=app.config['title'],
            intro=app.config['intro'])


def say(msg, arg=None):
    print(' - ' + msg.format(arg))


def is_valid_filename(fn):
    base, ext = path.splitext(fn)
    return ext.lstrip('.') in app.config['allow_extensions']


def upload_request(req):
    if 'file' not in req.files:
        say('{}', 'File not found')
        return 'File not found', 400
    f = req.files['file']
    fn = None
    if f.filename and app.config['allow_filenames']:
        fn = secure_filename(f.filename)
    if not fn:
        ts = datetime.now().strftime('%F-%H-%M-%S')
        fn = '{}.{}.bin'.format(ts, str(uuid4())[24:])
    if not is_valid_filename(fn):
        say('Invalid filename: {}', fn)
        return 'Invalid filename', 400
    fullpath = path.join(app.config['upload_dir'], fn)
    say('Saved: {}', fn)
    f.save(fullpath)
    return 'OK'


def get_config():
    return {
        'addr': environ.get('SERVER_ADDR', '0.0.0.0'),
        'port': int(environ.get('SERVER_PORT', '8000')),
        'title': environ.get('TITLE', 'Sup'),
        'intro': environ.get('INTRO', DEF_INTRO),
        'upload_dir': path.realpath(environ.get('UPLOAD_DIR', '/sup')),
        'upload_hook': environ.get('UPLOAD_HOOK', ''),
        'allow_filenames': bool(environ.get('ALLOW_FILENAMES', False)),
        'allow_extensions':
            environ.get('ALLOW_EXTENSIONS', DEF_EXTENSIONS).split() }


def main():
    debug = bool(environ.get('DEBUG', False))
    app.config.update(get_config())
    if not path.isdir(app.config['upload_dir']):
        print('upload directory does not exist', file=sys.stderr)
        sys.exit(1)
    say('Allowed extensions: {}', ' '.join(app.config['allow_extensions']))
    say('Allow user defined filenames: {}', app.config['allow_filenames'])
    say('Directory for uploads: {}', app.config['upload_dir'])
    say('URL prefix: {}', environ.get('URL_PREFIX', '/sup'))
    app.run(host=app.config['addr'], port=app.config['port'], debug=debug)


app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix=environ.get('URL_PREFIX', '/sup'))

if __name__ == '__main__':
    main()
