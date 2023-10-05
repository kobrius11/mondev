# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye
ARG run_as
RUN adduser $run_as
WORKDIR /app
# RUN chown $run_as:$run_as -R /app
# USER $run_as
COPY ./monda_live .
COPY ./requirements.txt .
RUN apt update
RUN apt install -y gettext
RUN pip3 install -r requirements.txt
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
