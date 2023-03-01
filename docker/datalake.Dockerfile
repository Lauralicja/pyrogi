FROM python:3.9.16-bullseye

WORKDIR /


RUN pip install azure-storage-file-datalake && \
    pip install azure-identity && \
    pip install azure-cli && \ 
    pip install python-dotenv

COPY /pyrogi/datalake /code

CMD [ "python", "/code/connection.py" ]