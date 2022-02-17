FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install virtualenv

RUN python3 -m venv venv

RUN . venv/bin/activate

RUN pip3 install -r requirements.txt

COPY . . 
 
CMD [ "python3", "wsgi.py" ]