FROM python:3.7.1

RUN apt-get update
RUN apt-get install -y nginx-light rabbitmq-server celeryd

RUN mkdir -p /dataset-manager /dataset-manager-assets/static
WORKDIR /dataset-manager

COPY ./requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY conf/dataset-manager.conf /etc/nginx/sites-enabled/
COPY conf/celeryd /etc/default/
RUN chmod 0640 /etc/default/celeryd

COPY ./ ./
ENV PYTHONUNBUFFERED=TRUE

RUN python manage.py collectstatic

RUN chown -R celery .
RUN chmod +x start.sh

EXPOSE 8000
CMD ./start.sh
