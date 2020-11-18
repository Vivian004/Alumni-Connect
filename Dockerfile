FROM python:3-onbuild
WORKDIR /app
COPY . /app
RUN pip install -r requirements-dev.txt
