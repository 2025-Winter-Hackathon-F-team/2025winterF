FROM python:3.11-slim
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app/