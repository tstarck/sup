FROM python:slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY sup.py .
COPY static static
COPY tmpl tmpl

EXPOSE 8000

ENTRYPOINT ["python", "sup.py"]
