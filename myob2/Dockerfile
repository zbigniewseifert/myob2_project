FROM ubuntu:latest

#MAINTAINER Zbigniew Seifert "z.seifert@gmail.com"
LABEL author="Zbigniew Seifert"

RUN apt-get update -y && \
    apt-get install -y python3-pip sqlite3 

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt && mkdir db && mkdir upload_files

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]
