FROM python:3.9.16-bullseye

WORKDIR /

RUN pip install kafka-python && \
    pip install redis && \ 
    pip install requests

COPY /pyrogi/ /code/

CMD ["python", "/code/producer/events.py"]