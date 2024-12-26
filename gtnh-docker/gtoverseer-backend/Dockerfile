FROM python:bookworm

WORKDIR /usr/src/app

RUN apt update && apt upgrade -y
RUN pip install --no-cache-dir flask psycopg2-binary

COPY . .
# COPY GTOverseer.py ./GTOverseer.py
# COPY api ./api
# COPY data ./data
# COPY routes ./routes
CMD [ "python", "./GTOverseer.py" ]
