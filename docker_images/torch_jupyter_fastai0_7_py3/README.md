# Docker Image torch_jupyter_fastai0_7_py3
Intended for use with Turi Bolt job submission for work on FastAI pt 2 2018 (FastAI0.7)

## Usage
1. `python submit.py -c config_old_fastai0_7.yml`
2. Wait for Bolt job to starts
3. Click link in Bolt logs to launch notebook
4. Start learning and enjoy all the setup time saved :D

## Environment
See environment.yml and Dockerfile for full setup documentation
- CUDA90
- miniconda w/ py3.6
- PyTorch (GPU)
- opencv
- kaggle-cli
- vim
- jupyter notebook (not lab!)

## Issues
pt2 of the 2018 course should just work!
One issue I had was course/dl2/fastai symbolic link was not copied from Blobby.
Fix: `!ln -sf /maxwellmckinnon/FastAInotebooks/fastai_maxfork/old/fastai /maxwellmckinnon/FastAInotebooks/fastai_maxfork/courses/dl2/fastai`
