FROM python:3.12.1

WORKDIR /app

COPY . /app

RUN pip3 install requirements.txt

EXPOSE 5000

CMD [ "python3", "app.py" ]