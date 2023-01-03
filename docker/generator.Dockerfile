FROM python:3.9.16-bullseye

WORKDIR /


COPY /pyrogi/ /code/

CMD ["python", "/code/main.py"]