FROM python:3.11

ADD app.py .

RUN pip install requests flask

CMD ["python", "app.py"]
