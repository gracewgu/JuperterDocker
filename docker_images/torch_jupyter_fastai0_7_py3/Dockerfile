FROM docker.apple.com/mdewitt/conda_py3_cuda90:latest

# Install tools
RUN apt-get update
RUN apt-get install -y apt-utils > /dev/null
RUN apt-get install -y tmux > /dev/null
RUN apt-get install -y vim > /dev/null
RUN apt-get install -y libsm6 libxext6
RUN sudo apt-get install -y libxrender-dev

# Install dependencies (keep default name so `conda activate` works)
RUN conda update -n base -c defaults conda
COPY environment_fastai0.7.yml .
RUN conda env update -f=environment_fastai0.7.yml -n='base'

RUN . /opt/conda/etc/profile.d/conda.sh && conda activate
# RUN conda install -c conda-forge jupyterlab

# Jupyter Lab extensions
# no thanks, 01/30/2019 huge issues with JLab not respecting conda environment's python.
# In same context notebook works fine, so going with that with a note to try Lab in a year
# RUN jupyter labextension install @jupyterlab/toc

# Setup aliases
RUN echo "alias blobby='aws --endpoint-url https://blob.mr3.simcloud.apple.com --cli-read-timeout 300'" >> ~/.bash_profile

# Copy the current directory contents.
COPY . .
