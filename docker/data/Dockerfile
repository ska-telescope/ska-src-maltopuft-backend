FROM node:22-alpine3.20

RUN apk update && npm install -g http-server 

ARG PORT=8081
EXPOSE ${PORT}

CMD http-server --port "${PORT}" --cors
