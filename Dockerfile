FROM python:3.7.1

RUN mkdir /dataset-manager
WORKDIR /dataset-manager

COPY ./requirements.txt ./
COPY ./database_requirements.txt ./
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY ./ ./
ENV PYTHONUNBUFFERED=TRUE

EXPOSE 8000
CMD python manage.py migrate && gunicorn datama.wsgi -b 0.0.0.0:8000
