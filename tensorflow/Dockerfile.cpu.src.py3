FROM gcr.io/tensorflow/tensorflow:latest-py3
MAINTAINER Erwan BERNARD

# ==============================================================================
# pythonlib/Dockerfile.cpu

# Pick up some dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
        build-essential cmake git nano \
        curl wget rsync unzip \
        libboost-all-dev \
        pkg-config \
        libgtk2.0-dev \
        # image codec
        libfreetype6-dev \
        libpng-dev \
        libzmq3-dev \
        libjpeg-dev \
        libjpeg8-dev \
        libtiff-dev \
        libjasper-dev \
        # library for video format convertion YUV ...
        libv4l-dev v4l-utils \
        # camera control
        libdc1394-22 libdc1394-22-dev \
        # Lapack
        libatlas-base-dev \
        # python
        python \
        python-dev \
        python-numpy \
        python-scipy \
        python-tk \
        python3 \
        python3-dev \
        python3-numpy \
        python3-scipy \
        python3-tk \
        python-setuptools \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install pip for python2 and 3
RUN wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate && \
    python get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

# install python2 tools
RUN pip2 --no-cache-dir install \
        numpy \
        matplotlib \
        scipy \
        scikit-image \
        docopt \
        schema \
        path.py \
        requests \
        bottle \
        tornado \
        ipython \
        ipykernel \
        jupyter \
        ptvsd==3.0.0 \
        h5py \
        && \
    python2 -m ipykernel install

# install python3 tools
RUN pip3 --no-cache-dir install \
        numpy \
        matplotlib \
        scipy \
        scikit-image \
        docopt \
        schema \
        path.py \
        addict \
        requests \
        bottle \
        tornado \
        ipython \
        ipykernel \
        jupyter \
        ptvsd==3.0.0 \
        h5py \
        && \
    python3 -m ipykernel install

RUN ldconfig

# configuration
ENV HOME "/home/dev"
RUN mkdir -p "$HOME"

ENV LIB_DIR "$HOME/lib"
RUN mkdir -p "$LIB_DIR"

WORKDIR $HOME/host

# RUN useradd dev && chown -R dev: /home/dev
# USER dev

RUN ln -snf /bin/bash /bin/sh
RUN cp /root/.bashrc $HOME/.bashrc && \
    sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/g' ~/.bashrc

CMD ["/bin/bash"]
# ==============================================================================
# opencv/Dockerfile.cpu

ENV OPENCV_DIR "$LIB_DIR/opencv"
RUN mkdir -p "$OPENCV_DIR"

# Pick up some dependencies
RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# download opencv3
RUN cd "$OPENCV_DIR" && \
    wget https://github.com/opencv/opencv/archive/master.zip && \
    unzip master.zip && \
    rm master.zip
    # git clone https://github.com/opencv/opencv.git  <-- don't work anymore : GnuTLS recv error

# download opencv3 contrib
RUN cd "$OPENCV_DIR" && \
    wget https://github.com/opencv/opencv_contrib/archive/master.zip && \
    unzip master.zip && \
    rm master.zip
    # git clone https://github.com/opencv/opencv_contrib.git  <-- don't work anymore : GnuTLS recv error

# build opencv3
# warning if we set BUILD_EXAMPLES=OFF cmake don't find IPP anymore (strange)
RUN cd "$OPENCV_DIR/opencv-master" && mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH="$OPENCV_DIR/opencv_contrib-master/modules" \
    -D BUILD_EXAMPLES=OFF \
    -D WITH_IPP=ON .. && \
    make -j$(nproc) && \
    make install && \
    /bin/bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf' && \
    ldconfig

# link ippicv
RUN ln -s "$OPENCV_DIR/opencv-master/3rdparty/ippicv/unpack/ippicv_lnx/lib/intel64/libippicv.a" "/usr/local/lib/libippicv.a"
# ==============================================================================
# redis/Dockerfile.cpu

# follow the tuto from here : https://redis.io/topics/quickstart

ENV REDIS_DIR "$LIB_DIR/redis-stable"

RUN cd "$LIB_DIR" && \
    wget http://download.redis.io/redis-stable.tar.gz && \
    tar xvzf redis-stable.tar.gz && \
    rm redis-stable.tar.gz && \
    cd redis-stable && \
    make -j"$(nproc)" && \
    make install

# install python2 tools
RUN pip2 --no-cache-dir install \
        redis

# install python3 tools
RUN pip3 --no-cache-dir install \
        redis
# ==============================================================================
# tensorflow/Dockerfile.cpu

# install python3 tools
RUN pip3 --no-cache-dir install -U \
    pandas \
    sklearn \
    h5py

# Keras
RUN pip3 install git+https://github.com/fchollet/keras.git

# install python2 tools
RUN pip2 --no-cache-dir install -U \
    pandas \
    sklearn \
    h5py

# Keras
RUN pip2 install git+https://github.com/fchollet/keras.git

# Set Tensorflow backend for Keras
ENV KERAS_BACKEND=tensorflow
