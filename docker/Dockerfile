FROM 2000cubits/raspbian:latest

COPY . /opt/app
WORKDIR /opt/app

RUN apt-get update \
    && apt-get install -y \
    autoconf autotools-dev \
    build-essential \
    gcc git \
    libasound2-dev libtool libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev libjpeg-dev zlib1g-dev \
    make \
    swig \
    && apt-get install -y python3-dev python3-pip python3-spidev \
    && apt-get install -y ruby

CMD ["tail", "-f", "/dev/null"]