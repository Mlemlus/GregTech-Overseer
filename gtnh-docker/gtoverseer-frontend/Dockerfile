FROM python:bookworm

WORKDIR /usr/src/app

RUN apt update && apt upgrade -y
RUN pip install --no-cache-dir altair pandas streamlit

COPY main.py ./main.py
COPY pages ./pages

HEALTHCHECK CMD curl --fail http://localhost/_stcore/health

CMD [ "streamlit", "run", "./main.py", "--server.port=80" ]
