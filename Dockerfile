FROM python:3.9.17-bookworm

ENV PYTHONBUFFERED True

ENV APP_HOME /query_api
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app