ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    build-base \
    python3-dev \
    gnupg \
    gpg-agent

WORKDIR /app


COPY requirements.txt ./

RUN pip3 install --break-system-packages -r requirements.txt

COPY main.py main.py
COPY automations.py automations.py

EXPOSE 8001

COPY run.sh /
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]