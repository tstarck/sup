#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: better headers, filename mangle support, add magic support

import sys

from os import environ, path
from uuid import uuid4
from datetime import datetime
from subprocess import run, CalledProcessError

from werkzeug.utils import secure_filename
from flask import (Blueprint, Flask,
    render_template, request, send_from_directory)


DEF_EXTENSIONS = 'asc bin txt log json yml yaml pdf gif jpg jpeg png gz xz zip'
DEF_INTRO = 'Please start the file upload by first selecting the file.'

PREFIX = environ.get('URL_PREFIX', '/sup')
blueprint = Blueprint('sup', __name__, template_folder='tmpl')


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/<filename>', methods=['GET'])
def index(filename=None):
    if request.method == 'POST':
        return upload_request(request)
    elif filename:
        return send_from_directory('static', filename)
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
    if app.config['upload_hook']:
        cmd = [app.config['upload_hook'], app.config['upload_dir'], fn]
        try:
            ret = run(cmd, check=True, encoding='utf-8')
        except CalledProcessError as cpe:
            say('{}', cpe)
            return 'Upload hook failed', 500
        except FileNotFoundError as fnfe:
            say('{}', fnfe)
            return 'Upload hook not found', 500
        except PermissionError as pe:
            say('{}', pe)
            return 'Upload hook permission failed', 500
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
            environ.get('ALLOW_EXTENSIONS', DEF_EXTENSIONS).split(),
        'MAX_CONTENT_LENGTH': 1024*1024*int(environ.get('MAX_FILE_SIZE', '1'))}


def main():
    debug = bool(environ.get('DEBUG', False))
    app.config.update(get_config())
    if not path.isdir(app.config['upload_dir']):
        print('upload directory does not exist', file=sys.stderr)
        sys.exit(1)
    say('URL prefix: {}', PREFIX)
    say('Upload hook: `{}`', app.config['upload_hook'])
    say('Upload directory: {}', app.config['upload_dir'])
    say('File size limit: {} B', app.config['MAX_CONTENT_LENGTH'])
    say('Allow user defined filenames: {}', app.config['allow_filenames'])
    say('Allowed extensions: {}', ' '.join(app.config['allow_extensions']))
    app.run(host=app.config['addr'], port=app.config['port'], debug=debug)


app = Flask(__name__)
app.register_blueprint(blueprint, url_prefix=PREFIX)

if __name__ == '__main__':
    main()
