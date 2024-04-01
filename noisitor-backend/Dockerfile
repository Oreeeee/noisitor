FROM python:3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["litestar", "run", "--host", "0.0.0.0"]
