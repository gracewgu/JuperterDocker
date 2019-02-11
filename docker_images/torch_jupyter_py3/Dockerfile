FROM docker.apple.com/mdewitt/conda_py3_cuda90:latest

# Install tools
RUN apt-get install -y apt-utils > /dev/null
RUN apt-get install -y tmux > /dev/null

# Install dependencies (keep default name so `conda activate` works)
COPY environment.yml .
RUN conda env update -f=environment.yml -n='base'
RUN . /opt/conda/etc/profile.d/conda.sh && conda activate

# Jupyter extensions
# RUN jupyter labextension install @jupyterlab/toc
RUN pip install -q --upgrade pip
RUN pip install -q jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install
