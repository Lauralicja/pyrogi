FROM python:3.9.16-bullseye

WORKDIR /

RUN pip install kafka-python 

COPY /pyrogi/consumer /code/
