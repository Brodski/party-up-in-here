####################################################################
# BUILD
# docker build --no-cache -t cbrodski/preper:v2023.1.11.1 -f Dockerfile_ECS_preper  .
# docker build --no-cache -t cbrodski/preper:official_v2 -f Dockerfile_ECS_preper  .

# DEBUG `RUN`
# docker run --env-file .\.env -e ENV=dev cbrodski/preper:v2023.1.11.1
# docker run --env-file .\.env -it -e ENV=dev cbrodski/preper:official_v2 /bin/bash

# PUSH
# docker push cbrodski/preper:official_v2
####################################################################
FROM python:3.10.13-bullseye

LABEL version="1.0"
LABEL description="Runs scraper"
LABEL maintainer="your-email@example.com"
LABEL url="https://github.com/Brodski/scraper-dl-vids"
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

######
# GO #
######
WORKDIR /app/party-up-in-here

# $ docker run <image-name> --file confg_varz.txt

ENTRYPOINT ["./entrypoint.sh"]

# CMD echo "NOT DONE!!!!!!!!!!!!" ; \
#     git reset --hard origin/master ; \
#     git pull origin master --force && \ 
#     python kickPreper.py ; \
#     echo "DONE!!!!!!!!!!!!" ; 
