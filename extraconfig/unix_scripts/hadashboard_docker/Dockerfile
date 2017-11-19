FROM resin/raspberrypi3-alpine-buildpack-deps:latest

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    rm -r /root/.cache

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
VOLUME /conf

# Copy source
COPY . .

#INSTALL

#RUN pip3 install .

CMD [ "appdaemon", "-c", "/conf"]
