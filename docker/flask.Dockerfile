FROM python:3.9.16-bullseye

WORKDIR /

RUN pip install redis && \ 
    pip install flask


COPY /generator/ /code/

CMD ["python", "/code/events_proxy.py"]

#CMD ["flask", "--app", "/code/events_proxy.py", "--debug", "run", "--host:0.0.0.0"]