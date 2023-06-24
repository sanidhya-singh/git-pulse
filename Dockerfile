# targets latest available Python version
FROM python:slim
LABEL maintainer=sanidhya235@gmail.com

# create directory for Dagster
RUN mkdir -p /opt/app/gitpulse

# copy Python environment requirements to container
COPY requirements.txt /opt/app/gitpulse

# change working directory
WORKDIR /opt/app/gitpulse

# setup and build environment
RUN apt-get update -y && \
 apt-get install sudo -y && \
 sudo apt-get install curl -y && \
 python -m pip install -r requirements.txt

# change working directory to src folder
WORKDIR /opt/app/gitpulse/src

# set DAGSTER_HOME environment variable to the DEV directory
ENV DAGSTER_HOME /opt/app/gitpulse/src/dagster_home