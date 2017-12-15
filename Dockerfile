FROM nlpbox/dplp

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install hug sh

WORKDIR /opt/dplp_service

ADD dplp_hug_api.py /opt/dplp_service
EXPOSE 8000

# FIXME: add this to nlpbox/dplp repo
ADD dplp.sh output_break.txt /opt/DPLP/

ENTRYPOINT ["hug"]
CMD ["-f", "dplp_hug_api.py"]
