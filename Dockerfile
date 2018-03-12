FROM python

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sup.py .
COPY static static
COPY tmpl tmpl

EXPOSE 8000

VOLUME /sup

ENTRYPOINT ["python", "sup.py"]
