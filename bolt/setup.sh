#!/bin/bash -e
###
# Install any necessary dependencies.
###
echo "------- Running setup.sh -------"

. /opt/conda/etc/profile.d/conda.sh
conda activate
pip install -q --upgrade pip

# Export for future sessions.
echo "export PATH=$PATH:$TASK_RUNTIME_DIR/util" >> ~/.bashrc # Add bolt utilities to the path.
echo "export blobby='aws --endpoint-url https://blob.mr3.simcloud.apple.com --cli-read-timeout 300'" >> ~/.bashrc
source ~/.bashrc

# Copy the contents of the requested bucket at `BUCKET_PATH`.
. copy_blobby_bucket

# Install additional dependencies silently.
# conda install ... --yes > /dev/null
# pip install -q ...
