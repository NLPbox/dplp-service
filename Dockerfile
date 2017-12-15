FROM nlpbox/dplp:latest

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install hug sh

WORKDIR /opt/dplp_service

ADD dplp_hug_api.py /opt/dplp_service
EXPOSE 8000

ENTRYPOINT ["hug"]
CMD ["-f", "dplp_hug_api.py"]
