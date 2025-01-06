FROM python:bookworm

WORKDIR /usr/src/app

RUN apt update && apt upgrade -y
RUN pip install --no-cache-dir flask psycopg2-binary requests

COPY . .
CMD [ "python", "./GTOverseer.py" ]
