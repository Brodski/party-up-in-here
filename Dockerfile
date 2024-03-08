####################################################################
# BUILD
# docker build --no-cache -t cbrodski/party-up:v1 -f Dockerfile  .

# DEBUG `RUN`
# docker run -d --entrypoint tail -v ${PWD}/configs:/app/party-up-in-here/configs cbrodski/party-up:v1 -f /dev/null
# AND THEN THIS
# docker exec -it <a898649aeb40> /bin/bash

# PUSH
# docker push cbrodski/party-up:v1

# RUN?
# $ docker run <image-name> --file confg_varz.txt
# $ docker run cbrodski/party-up:v1 --file myEmail_1.conf -d -v $(pwd)/configs:/app/party-up-in-here/configs
# $ docker run -v ${pwd}\configs:/app/party-up-in-here/configs  cbrodski/party-up:v1 --which-action create --file myEmail_1.conf     

####################################################################
FROM python:3.10.13-bullseye

LABEL version="1.0"
LABEL description="Runs it"
LABEL maintainer="your-email@example.com"
LABEL url="https://github.com"
LABEL build_date="2024-01-01"
LABEL vendor="Bski Inc."
LABEL license="Bski"


###########
# Project #
###########
WORKDIR /app
RUN apt update 
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata 
RUN apt install git -y 
RUN git clone https://github.com/Brodski/party-up-in-here.git
WORKDIR /app/party-up-in-here
RUN git config pull.rebase false
RUN chmod +x ./entrypoint.sh

#######
# Pip #
#######    
WORKDIR /app
RUN apt install curl  -y 
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py pip==23.0.1 \
    && pip --version \
    && rm get-pip.py 
    
################
# Dependencies #
################
WORKDIR /app/party-up-in-here
RUN pip install -r requirements.txt
RUN apt-get install -y firefox-esr

# RUN apt-get install -y x11-apps
# RUN apt-get install -y x11-xserver-utils
# ENV DISPLAY=:0

######
# GO #
######
WORKDIR /app/party-up-in-here

ENTRYPOINT ["./entrypoint.sh"]
