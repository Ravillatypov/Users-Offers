FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc make libc-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app

COPY ./main.py /app

RUN adduser -D offersapp
USER offersapp
EXPOSE 8000
ENTRYPOINT ["python", "/app/main.py"]
