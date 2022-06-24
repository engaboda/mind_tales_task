FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /backend

# System dependencies are updated less often than python dependencies
RUN apt-get update \
    && pip3 install --upgrade pip \
    && apt install netcat -y


# Python dependencies are updated less often than source code
COPY . /backend/
RUN pip3 install -r requirements/base.txt
