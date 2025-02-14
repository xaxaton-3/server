FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /defenders
WORKDIR /defenders

COPY requirements.txt /defenders/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /defenders