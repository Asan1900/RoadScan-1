FROM osgeo/gdal
MAINTAINER Tima  "temirlan.abdrakmanovv@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN set -xe \
    && apt-get update \
    && apt-get install -y python3.10 \
    && apt-get install -y python3-pip
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN apt-get install -y gdal-bin python3-gdal
RUN pip install -r requirements.txt
RUN apt install libsqlite3-mod-spatialite
RUN #pip install psycopg2-binary
ADD . /code/
EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]