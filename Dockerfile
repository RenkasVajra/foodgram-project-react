FROM python:3.8.5

RUN pip install --upgrade pip

RUN mkdir /code

COPY requirements.txt /code

RUN pip3 install -r /code/requirements.txt

COPY . /code

WORKDIR /code

RUN python --version; pip --version

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000