FROM registry.cn-shanghai.aliyuncs.com/shenminjun/fl_base:1.5

USER root

COPY ./ /tff_client

WORKDIR /tff_client

RUN pip install -r requirements.txt

CMD python3 run.py

EXPOSE 5000
