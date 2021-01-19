FROM python:latest
RUN apt-get update && apt-get -y install unixodbc-dev && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && apt-get -y update && ACCEPT_EULA=Y apt-get -y install msodbcsql17 && ACCEPT_EULA=Y apt-get -y install mssql-tools && apt-get -y install unixodbc-dev && apt-get -y install libgssapi-krb5-2
WORKDIR /app
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
#ADD odbcinst.ini /etc/odbcinst.ini
COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
