FROM python:3.11

ADD test.py .

RUN pip install requests

CMD ["python", "test.py"]
