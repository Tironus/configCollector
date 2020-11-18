FROM        docker.io/ubuntu:latest

ENV         container docker
ENV         CONFIG_COMMANDER=ccommander
ENV         CONFIG_COMMANDER_PORT=31083

RUN         apt update && \
            apt install -y build-essential python3 python3-pip git && \
            git clone https://github.com/Tironus/configCollector.git && \
            cd ./configCollector && \
            make install && \
            cd config_collector_api

EXPOSE      8001/tcp

CMD         cd /configCollector/config_collector_api && uvicorn configCollectorAPI:app --host 0.0.0.0 --port 8001 --reload