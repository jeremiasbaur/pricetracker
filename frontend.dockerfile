FROM node:12.2.0-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./client/package*.json ./

RUN npm install

COPY /client /app/

#RUN vue add bootstrap-vue

CMD ["npm", "run", "serve"]
