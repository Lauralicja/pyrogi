FROM python:3.9.16-bullseye

WORKDIR /


RUN pip install azure-storage-file-datalake

COPY /pyrogi .

CMD ["python", "./main.py"]