FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc make libc-dev && \
    pip install -r /requirements.txt && \
    apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app

COPY ./main.py /app

RUN adduser -D offersapp
USER offersapp
EXPOSE 8000
ENTRYPOINT ["python", "/app/main.py"]
