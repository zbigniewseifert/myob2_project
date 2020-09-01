FROM alpine:latest
RUN apk add --no-cache python3  bash && \
apk --update add --virtual build-dependencies  py3-pip sqlite

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt && mkdir db && mkdir upload_files

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "application.py" ]
