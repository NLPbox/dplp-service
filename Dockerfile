FROM nlpbox/dplp:2018-11-17

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install hug sh pexpect pytest requests sh

WORKDIR /opt/dplp_service

ADD dplp_hug_api.py test_api.py /opt/dplp_service/
EXPOSE 8000

RUN pip3 install pudb ipython # TODO: rm

ENTRYPOINT ["hug"]
CMD ["-f", "dplp_hug_api.py"]
