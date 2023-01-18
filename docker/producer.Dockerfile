FROM confluentinc/cp-kafka:7.3.0

WORKDIR /

RUN pip install kafka-python


COPY /pyrogi/producer/ /code/

CMD ["python", "/code/users.py"]

#CMD ["flask", "--app", "/code/events_proxy.py", "--debug", "run", "--host:0.0.0.0"]