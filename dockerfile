FROM python:3.7
LABEL maintainer="barrabrawa@gmail.com"
COPY . /flask_app
WORKDIR /flask_app
RUN pip install -r requirements.txt
EXPOSE 8180
EXPOSE 8181
VOLUME /app/app/models
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]