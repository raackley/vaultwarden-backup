FROM python:3-slim

LABEL maintainer="ryan@ryanackley.com"

ADD src/ .

RUN python -m pip install -r requirements.txt

RUN apt update && apt install sqlite3 -y

CMD python vaultwarden-backup.py