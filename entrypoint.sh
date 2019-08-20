#!/bin/sh
uwsgi \
  --master --socket 0.0.0.0:${PORT:-5000} \
  --wsgi-file sup.py --callable app \
  --uid www-data --gid www-data \
  --processes ${PROC:-1}
