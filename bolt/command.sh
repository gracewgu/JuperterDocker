#!/bin/bash -e
###
# Commands run when the job starts.
###
echo "------- Running command.sh -------"

# Start a Tensorboard session that you can attach to later.
# - Note: Installing outside the conda env can help with conflicting requirements.
# pip -q install tensorflow
# tensorboard --logdir /runs --port $TENSORBOARD_PORT &
# echo "Tensorboard live at: http://${SC_HOSTNAME}:${TENSORBOARD_PORT}"

. /opt/conda/etc/profile.d/conda.sh
conda activate

source ~/.bashrc

# Start a backup sync running every BACKUP_INTERVAL_SEC.
blobby_sync --interval $BACKUP_INTERVAL_SEC &

# Run a job and save output to BOLT_ARTIFACT_DIR.
# execute_notebook "<Your Notebook>.ipynb" -o "${BOLT_ARTIFACT_DIR}/run.ipynb" --to html

# To run any copied files, use the full path for the `TASK_RUNTIME_DIR`.
# python3 $TASK_RUNTIME_DIR/example.py

# Start the notebook server from the requested bucket.
if [ $BUCKET_PATH ]; then
    cd /$BUCKET_PATH
fi
# - Note: `.` sources the script to this process and holds execution as long the notebook is running.
# (Keeping the bolt job alive)
. start_notebook_server

# Finish execution stopping any background jobs from keeping the bolt task alive.
if [ $(jobs -p) ]; then
    kill $(jobs -p)
fi
