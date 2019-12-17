FROM python:3

RUN mkdir /project
WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update
RUN ln -snf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && echo "America/Sao_Paulo" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
RUN apt --only-upgrade install tzdata

RUN pip install --upgrade pip
COPY ./config/requirements.txt /project/requirements.txt 
RUN pip install -r /project/requirements.txt && rm /project/requirements.txt 

EXPOSE 8000 443