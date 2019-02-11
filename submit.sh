#!/bin/bash -e

simcloud job run \
    --docker-image docker.apple.com/mdewitt/torch_jupyter_py3:latest \
    --cpus 2 \
    --gpus 1 \
    --ssh \
    --ports 8888 \
    --timeout 1d
