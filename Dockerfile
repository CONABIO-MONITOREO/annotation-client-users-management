FROM python:3.12

RUN apt-get update && \
    apt-get install -y \
        postgresql-client \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /api

COPY .env .env
COPY requirements.txt requirements.txt
COPY / .

RUN pip install -r requirements.txt

COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

EXPOSE 5000
