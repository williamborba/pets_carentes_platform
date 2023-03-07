FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update
RUN ln -snf /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && echo "America/Sao_Paulo" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
RUN apt --only-upgrade install tzdata

RUN pip install --upgrade pip && pip install --root-user-action=ignore  \
    avinit[png] a2wsgi boto3==1.26.74 coverage==7.1.0 gunicorn httpx firebase-admin==6.1.0 kink \
    motor==3.1.1 pytest==7.2.1 pytest-asyncio PyJWT==2.6.0 python-bsonjs pyyaml Pillow==9.4.0 pydantic==1.10.5  \
    pymongo==4.3.3 python-multipart rq==1.13.0 requests==2.28.2 redis==4.5.1 starlette[full]==0.25.0  \
    sentry-sdk[starlette]==1.15.0 uvicorn==0.20.0

WORKDIR /project

EXPOSE 8000 443
