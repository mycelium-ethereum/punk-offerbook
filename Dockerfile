FROM python:3.7-stretch
COPY . /app
WORKDIR /app
EXPOSE 3400
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt update -y
RUN apt install -y build-essential curl cron
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup update
RUN pip3 install -r requirements.txt
ADD ./shell-scripts/crontab /etc/cron.d/simple-cron
ADD ./shell-scripts/event_master.sh /event_master.sh
ADD ./shell-scripts/refresh_master.sh /refresh_master.sh
ADD ./shell-scripts/start_server.sh /start_server.sh
RUN chmod +x /event_master.sh /refresh_master.sh /start_server.sh 
RUN chmod 0644 /etc/cron.d/simple-cron
RUN touch /var/log/cron.log
RUN python3 store_volume_data.py
CMD cron && tail -f /var/log/cron.log

# CMD ["uvicorn", "floor_price:app", "--host", "0.0.0.0", "--port", "3400"]