FROM python:3.7

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt-get install -qy \
    build-essential \
    tcpdump

RUN pip install \
    coloredlogs \
    aiohttp \
    asyncio \
    scapy \
    memory_profiler \
    asyncpg

RUN mkdir /pahan/
WORKDIR /pahan/

EXPOSE 8888

ADD traffic/ traffic/
ADD web/ web/
ADD backends/ backends/
# RUN mkdir logs/
# ADD dumps/ dumps/
ADD pahan.py pahan.py
ADD settings.py settings.py

CMD python /pahan/pahan.py
