# Support TuriBolt
# https://gitlab-turi.corp.apple.com/turi/bolt-sample/tree/master/docker-gpu
FROM docker.apple.com/turibolt/base/ubuntu16.04:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# Miniconda w/ python 3.6
# Setup from the official Continuum docker distribution:
# https://github.com/ContinuumIO/docker-images/blob/master/miniconda3/Dockerfile 
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# Instructions from https://www.tensorflow.org/install/gpu
# Add NVIDIA package repository
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub \
 && wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
 && apt install -y ./cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
 && wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb \
 && apt install -y ./nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb \
 && apt update -y

# Install CUDA and tools. Include optional NCCL 2.x
RUN apt install -y cuda9.0 cuda-cublas-9-0 cuda-cufft-9-0 cuda-curand-9-0 \
    cuda-cusolver-9-0 cuda-cusparse-9-0 libcudnn7=7.2.1.38-1+cuda9.0 \
    libnccl2=2.2.13-1+cuda9.0 cuda-command-line-tools-9-0

RUN rm cuda-repo-ubuntu1604_9.1.85-1_amd64.deb \
    nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb
