FROM python:2.7

RUN apt-get update
RUN apt-get install daemontools

##### End of OS-level cacheable instructions #####

RUN mkdir -p /opt/progcom
ADD ./requirements.pip /opt/progcom
RUN pip2 install -r /opt/progcom/requirements.pip

##### End of Python-level cacheable instructions #####

EXPOSE 4000
WORKDIR /opt/progcom
CMD envdir docker-config ./app.py

##### End of Command #####
##### Sensitive to changes #####

ADD . /opt/progcom
