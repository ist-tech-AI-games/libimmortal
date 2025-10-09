FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04
SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND noninteractive
ENV MPLLOCALFREETYPE 1
RUN sed -i 's|http://archive.ubuntu|http://mirror.kakao|g' /etc/apt/sources.list
RUN sed -i 's|http://security.ubuntu|http://mirror.kakao|g' /etc/apt/sources.list

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/opt/conda/bin:$PATH
ENV TZ=Asia/Seoul

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y wget unzip zip
RUN apt-get update --fix-missing

# Install basic packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      build-essential make cmake clang gcc-10 g++-10 \
      wget curl ca-certificates git unzip zip \
      libssl-dev zlib1g-dev \
      libbz2-dev libreadline-dev libsqlite3-dev \
      libncurses5-dev libncursesw5-dev \
      libffi-dev liblzma-dev xz-utils tk-dev \
      libgdbm-dev libgdbm-compat-dev uuid-dev \
      htop tmux vim nvtop && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3.10.12
ARG PY_VER=3.10.12
RUN set -euo pipefail && \
    cd /tmp && \
    wget -q https://www.python.org/ftp/python/${PY_VER}/Python-${PY_VER}.tgz && \
    tar -xf Python-${PY_VER}.tgz && cd Python-${PY_VER} && \
    ./configure --prefix=/usr/local --enable-optimizations --with-lto && \
    make -j"$(nproc)" && \
    make altinstall && \
    /usr/local/bin/python3.10 -m ensurepip --upgrade && \
    /usr/local/bin/python3.10 -m pip install -U pip setuptools wheel && \
    cd / && rm -rf /tmp/Python-${PY_VER} /tmp/Python-${PY_VER}.tgz

# 편의용 심볼릭 링크 (컨테이너 내부 기본 python/pip을 3.10로 사용)
RUN ln -sf /usr/local/bin/python3.10 /usr/local/bin/python3 && \
    ln -sf /usr/local/bin/pip3.10    /usr/local/bin/pip3

RUN apt-get update --fix-missing
RUN apt-get upgrade -y

RUN apt-get install sudo
RUN apt-get update
RUN apt-get autoremove  

# Copy and install requirements.txt
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt
RUN rm /root/requirements.txt

# Install Pytorch
RUN pip3 install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu121

# Download linux game build
RUN wget https://github.com/ist-tech-AI-games/immortal_suffering/releases/download/v.1.0/immortal_suffering_linux_x86_64.zip
RUN unzip immortal_suffering_linux_x86_64.zip -d /root/immortal_suffering
RUN chmod -R 755 /root/immortal_suffering/immortal_suffering_linux_build.x86_64

# Install Xvfb
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb x11vnc fluxbox \
    mesa-utils libgl1-mesa-glx libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

COPY docker/start_xvfb.sh /usr/local/bin/start_xvfb.sh
RUN chmod +x /usr/local/bin/start_xvfb.sh

ENV LIBGL_ALWAYS_SOFTWARE=1

# remove cache
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/local/bin/start_xvfb.sh"]
CMD ["bash"]

WORKDIR /root

# Clone libimmortal repo
COPY . /root/libimmortal
WORKDIR /root/libimmortal
RUN pip3 install -e .

WORKDIR /root