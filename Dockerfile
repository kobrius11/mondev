# syntax=docker/dockerfile:1
FROM python:slim-bullseye
ARG run_as
RUN adduser $run_as
WORKDIR /app
COPY ./monda_live .
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN chown $run_as:$run_as -R /app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
