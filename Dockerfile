FROM python:3.7

COPY . /app

WORKDIR /app

RUN cat .env

RUN ls -lh

CMD bash -c "pip3 install -r requirements.txt && gunicorn -w 4 -b 0.0.0.0:5000 app:app"