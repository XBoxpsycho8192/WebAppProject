FROM python:3.11-slim-buster
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 8081
CMD python ./app.py
