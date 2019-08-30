FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -qy \
    python3-dev \
    python3-pip \
    build-essential \
    tshark 

RUN pip3 install \
    coloredlogs \
    aiohttp \
    asyncio

RUN mkdir /pahan/
WORKDIR /pahan/

ADD traffic/ traffic/
ADD web/ web/
# RUN mkdir logs/
# ADD dumps/ dumps/
ADD pahan.py pahan.py
ADD settings.py settings.py

CMD python3 /pahan/pahan.py
