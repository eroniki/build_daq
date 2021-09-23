FROM python:3.9.6-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    tini \
    supervisor

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN env
COPY core/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir "${LOG_FOLDER_CONTAINER}"
WORKDIR "/home/${DOCKER_USER}"
ENTRYPOINT ["tini", "-s", "--"]
# CMD ["python", "-m", "app"]
CMD ["bash"]
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
