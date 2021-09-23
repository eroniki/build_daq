FROM nvidia/cuda:10.0-cudnn7-devel

ENV DEBIAN_FRONTEND=noninteractive
# install system packages
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    software-properties-common \
    curl \
    python3-dev \
    python3-pip \
    python3-tk \
    locales \
    build-essential \
    cmake \
    libssl-dev \
    libprotobuf-dev \
    libleveldb-dev \
    libsnappy-dev \
    libhdf5-serial-dev \ 
    protobuf-compiler \
    libboost-all-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    liblmdb-dev \
    opencl-headers \
    ocl-icd-opencl-dev \
    libviennacl-dev \
    libopencv-dev \
    wget \
    git \
    libatlas-base-dev \
    && ldconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/tools/
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install --upgrade pip

RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN python -m pip install --upgrade pip
FROM python:3.9.6-slim-buster

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    tini

ENV USER=discotech
WORKDIR /home/${USER}
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["tini", "-s", "--"]
CMD ["/bin/bash"]
