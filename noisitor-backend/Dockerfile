FROM python:3.12
WORKDIR /app
RUN apt-get update
RUN apt-get install libpq5 -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["litestar", "run", "--host", "0.0.0.0"]
