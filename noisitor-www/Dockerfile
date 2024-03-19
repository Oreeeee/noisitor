FROM debian:12
WORKDIR /app
RUN apt-get update
RUN apt-get install python3 python3-pip nodejs npm -y
COPY requirements.txt requirements.txt
RUN pip install --break-system-packages -r requirements.txt
COPY . /app
WORKDIR /app/www
RUN npm i
RUN npm run build
WORKDIR /app
CMD ["litestar", "run", "--host", "0.0.0.0"]
