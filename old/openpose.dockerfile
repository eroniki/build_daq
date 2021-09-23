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

RUN wget -c "https://github.com/Kitware/CMake/releases/download/v3.19.6/cmake-3.19.6.tar.gz"
RUN tar xf cmake-3.19.6.tar.gz
RUN cd cmake-3.19.6 && ./configure && make -j `nproc` && make install

# get the DAQ code
WORKDIR /home/build_daq
RUN git clone https://github.com/eroniki/build_daq.git .
RUN python -m pip install -r requirements.txt
RUN python3 -m pip install -r requirements.txt

#get openpose
WORKDIR /home/openpose
RUN git clone https://github.com/eroniki/openpose.git .
RUN git submodule update --init --recursive

#build it
WORKDIR /home/openpose/build
RUN cmake -DBUILD_PYTHON=ON \
    -DPYTHON_EXECUTABLE=/usr/bin/python2.7 \
    -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython2.7m.so ..
RUN make -j `nproc`
RUN make install
RUN ldconfig
WORKDIR /home/openpose/build/python/openpose
RUN make install
