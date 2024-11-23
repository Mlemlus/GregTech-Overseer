FROM python:bookworm

WORKDIR /usr/src/app

RUN apt update && apt upgrade -y
RUN pip install --no-cache-dir flask psycopg2-binary

COPY GTOverseer.py ./GTOverseer.py
COPY data_process ./data_process
COPY database ./database
CMD [ "python", "./GTOverseer.py" ]
