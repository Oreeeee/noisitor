FROM python:3.12-slim
WORKDIR /app
RUN apt-get update
RUN apt-get install tshark -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["python3", "noisitord.py"]
