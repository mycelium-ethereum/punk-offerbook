FROM python:3.7-stretch
COPY . /app
WORKDIR /app
RUN mkdir logs
EXPOSE 8080
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt update -y
RUN apt install -y build-essential curl cron
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup update
RUN pip3 install -r requirements.txt
ADD ./docker-scripts/crontab /etc/cron.d/simple-cron
RUN chmod +x ./docker-scripts/event_master.sh 
RUN chmod +x ./docker-scripts/refresh_master.sh
RUN chmod +x ./docker-scripts/start_server.sh
RUN chmod +x ./docker-scripts/store_volume.sh
RUN chmod +x ./docker-scripts/setup.sh
RUN chmod 0644 /etc/cron.d/simple-cron
RUN touch /var/log/cron.log
CMD ./docker-scripts/setup.sh
# CMD cron && ./docker-scripts/refresh_master.sh && ./docker-scripts/store_volume.sh && tail -F /var/log/cron.log