FROM python:3.9.16-bullseye

WORKDIR /

RUN pip install pydantic && \ 
    pip install faker && \ 
    pip install redis


COPY /generator/ /code/

CMD ["python", "/code/generator.py"]