FROM python:latest
RUN apt-get update && apt-get -y install unixodbc-dev
WORKDIR /app
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]