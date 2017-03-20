FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt
ADD . /code/
