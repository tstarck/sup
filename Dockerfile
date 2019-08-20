FROM python:slim

COPY requirements.txt .
RUN set -x \
  && apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential \
  && pip install --no-cache-dir -r requirements.txt \
  && apt-get remove -y build-essential \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc

WORKDIR /app
COPY sup.py .
COPY entrypoint.sh .
COPY static static
COPY tmpl tmpl

RUN set -x && chmod -c 0755 entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
