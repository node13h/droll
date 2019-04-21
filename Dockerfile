FROM python:3.7.3-alpine

ARG VERSION
COPY dist/droll-${VERSION}.tar.gz /sdist/droll.tar.gz

VOLUME /static

RUN apk --update add --no-cache postgresql-dev gcc musl-dev && pip3 install psycopg2 && apk del postgresql-dev gcc musl-dev

RUN apk --update add --no-cache postgresql

RUN pip3 install /sdist/droll.tar.gz

EXPOSE 8080

ENTRYPOINT ["gunicorn", "droll.application.wsgi"]
