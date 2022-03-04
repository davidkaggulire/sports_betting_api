FROM python:3.8-slim-buster

WORKDIR /app

ENV GOOGLE_APPLICATION_CREDENTIALS=$CERTIFICATE_BASE64

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . . 
 
CMD [ "python3", "wsgi.py" ]