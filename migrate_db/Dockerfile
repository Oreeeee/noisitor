FROM python:3.12
WORKDIR /app
RUN apt-get update
RUN apt-get install libpq5 -y
COPY requirements.txt requirements.txt
COPY convert.py convert.py
RUN pip install -r requirements.txt
CMD ["python", "convert.py"]
