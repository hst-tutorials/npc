FROM --platform=arm64 python:slim-bullseye

#Install prereqs
RUN apt-get update && apt-get install -y python3-pip iperf3 curl iputils-ping
RUN curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash && apt-get install -y speedtest

#Copy data into image

COPY app/ /app

RUN python3 -m pip install -r /app/requirements.txt


CMD [ "python3", "-u", "/app/app.py" ]