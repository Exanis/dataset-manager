FROM python:3.7.1

RUN apt-get update
RUN apt-get install -y nginx-light

RUN mkdir /dataset-manager /dataset-manager-assets
WORKDIR /dataset-manager

COPY ./requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY conf/dataset-manager.conf /etc/nginx/sites-enabled/

COPY ./ ./
ENV PYTHONUNBUFFERED=TRUE

RUN python manage.py collectstatic

EXPOSE 8000
CMD ./start.sh
