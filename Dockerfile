FROM python:3.7-stretch
COPY . /app
WORKDIR /app
EXPOSE 3400
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt update -y
RUN apt install -y build-essential curl
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup update
RUN pip3 install -r requirements.txt
# add crontab here
CMD ["uvicorn", "floor_price:app", "--host", "0.0.0.0", "--port", "3400"]