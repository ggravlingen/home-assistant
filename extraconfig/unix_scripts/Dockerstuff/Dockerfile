# Prereq: copy virtualization folder from home-assistant folder

FROM armhf/ubuntu:latest

RUN apt-get update -y && \
  apt-get install -y python3 python3-pip git autoconf automake libtool wget apt-utils mlocate && \
  apt-get clean -y && \
  pip3 install --upgrade pip && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* build/

# Uncomment any of the following lines to disable the installation.
ENV INSTALL_TELLSTICK no
ENV INSTALL_OPENALPR no
ENV INSTALL_FFMPEG no
ENV INSTALL_OPENZWAVE no
ENV INSTALL_LIBCEC no
ENV INSTALL_PHANTOMJS no

VOLUME /config

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy build scripts
COPY virtualization/Docker/ virtualization/Docker/
RUN virtualization/Docker/setup_docker_prereqs

# Install hass component dependencies
COPY requirements_all.txt requirements_all.txt
RUN pip3 install homeassistant
#RUN pip3 install --no-cache-dir -r requirements_all.txt
## && \
#    pip3 install --no-cache-dir mysqlclient psycopg2 uvloop cchardet

# Copy source
COPY . .

#CMD [ "python", "-m", "homeassistant", "--config", "/config" ]
