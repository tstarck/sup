#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: log more

from os import environ, path
from sys import exit
from uuid import uuid4
from datetime import datetime

from flask import Blueprint, Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

E_NOFILE = 'File not found'
E_FILENAME = 'Filename not allowed'
DEF_EXTENSIONS = 'asc txt log pdf gif jpg jpeg png gz xz zip'

#blueprint = Blueprint('sup', __name__, template_folder='templates')

app = Flask(__name__)
#app.register_blueprint(blueprint, blueprint='FIXME')


def is_valid_filename(fn):
    base, ext = path.splitext(fn)
    return ext.lstrip('.') in app.config['valid_extensions']

def upload(req):
    if 'file' not in req.files:
        flash(E_NOFILE)
        return redirect(req.url)
    f = req.files['file']
    fn = None
    if f.filename and app.config['allow_filenames']:
        fn = secure_filename(f.filename)
    if not fn:
        ts = datetime.now().strftime('%F-%H-%M-%S')
        fn = '{}.{}.bin'.format(ts, str(uuid4())[24:])
    if not is_valid_filename(fn):
        flash(E_FILENAME)
        return redirect(req.url)
    fullpath = path.join(app.config['upload_dir'], fn)
    f.save(fullpath)
    return 'OK'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return upload(request)
    else:
        return render_template('upload.html')


def main():
    # CONFIG: default filename, title text
    upload_dir = environ.get('UPLOAD_DIR', '/sup')
    app.config['addr'] = environ.get('SERVER_ADDR', '0.0.0.0')
    app.config['port'] = int(environ.get('SERVER_PORT', '8000'))
    app.config['allow_filenames'] = bool(environ.get('ALLOW_FILENAMES', False))
    app.config['valid_extensions'] = environ.get('ALLOW_EXTENSIONS', DEF_EXTENSIONS).split()
    app.config['title'] = environ.get('TITLE', 'FIXME')

    if path.isdir(upload_dir):
        app.config['upload_dir'] = environ.get('UPLOAD_DIR', '/sup')
    else:
        print('error: upload directory does not exist', file=sys.stderr)
        exit(1)

    app.run(host=app.config['addr'], port=app.config['port'], debug=True)

if __name__ == '__main__':
    main()
