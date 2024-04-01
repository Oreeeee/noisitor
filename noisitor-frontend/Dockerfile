FROM node:21
WORKDIR /app
COPY . /app
RUN npm i
RUN npm run build
CMD ["node", "build/index.js"]
