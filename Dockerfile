FROM nlpbox/dplp:latest

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install hug sh

WORKDIR /opt/dplp_service

RUN pip3 install ipython pudb # TODO: rm after debug
ADD pudb.cfg /root/.config/pudb

RUN apt-get install -y xvfb imagemagick python-tk python-pip
RUN pip2 install ipython pudb # TODO: rm after debug

ADD dplp_hug_api.py /opt/dplp_service
EXPOSE 8000

ENTRYPOINT ["hug"]
CMD ["-f", "dplp_hug_api.py"]
