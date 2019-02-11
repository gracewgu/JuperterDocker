# README

Create a new Jupyter instance on either Turi Bolt or Simcloud configured with a docker image.

## Docker Zoo

Python3.7.2 + PyTorch1.0 + JupyterLab (default in config.yaml)
`docker.apple.com/mdewitt/torch_jupyter_py3@sha256:abba8505ec0645a1d41ba64725fb98fbb4054d428d7a16a3755f837add0e5b31` :v2

Python3.7.2 + PyTorch1.0 + JupyterLab + fastai1.0.42 + tensorboardX
`docker.apple.com/mdewitt/fastai@sha256:c36b1d22027a0489f56ad0354efcb1a59f3fed9c921f6955d64c2a0f9e763d67` :v0

Python3.6.8 + PyTorch0.3.1.post2 + Jupyter + fastai0.7 (config_old_fastai0_7.yml)
`docker.apple.com/mmcki/torch_jupyter_py3_fastai0_7@sha256:598074e68541a5f333a7fff96c2353baf38bf59b83331733264bc32070ba214d`

## Bolt Submission

After cloning the repo, navigate to the project root.

Run the following code in a local **python3.6** environment. Python3.7 is not compatible yet. (<rdar://problem/46545623>)

Requires Bolt 1.13+

``` python
pip install --upgrade turibolt --index https://pypi.apple.com/simple
```

``` bash
cd bolt/
python submit.py
```

The job has been queued onto the `bolt` infrastructure. In order to get the jupyter environment:

1. Login to [turibolt](https://bolt.apple.com).
2. You should see a new job enqueued.
3. Once the job is running, click the job to go into the job details.
4. Go to the `Logs` tab.
5. Go to the `user/notebook_credentials.log`

You should see something like:

```bash
*************************************************************************
Notebook ready in Bolt task: 9wrrmybpuy
The simcloud Jupyter notebook server is ready for you at:
http://mr3-409-0518-15-srv.mr3.simcloud.apple.com:21213/?token=c......  # token redacted

Bolt task url: https://bolt.apple.com/tasks/9wrrmybpuy/details
Connect to ssh using: ssh -i ~/.turibolt/bolt_ssh_key -p 23916 root@mr3-409-0518-15-srv.mr3.simcloud.apple.com
Tensorboard: http://mr3-409-0518-15-srv.mr3.simcloud.apple.com:38634
*************************************************************************
```

In a browser, simply go to `http://mr3-409-0518-15-srv.mr3.simcloud.apple.com:21213/?token=c...` and your jupyter lab environment will be available.

### Workflow

When creating your own job it's often easiest to copy the *config.yaml* and local scripts to customize for your project. You may also wish to alias the submit command as follows:

``` bash
# Within bolt/
BOLT_SUBMIT_PATH=${PWD}/submit.py
alias bolt_submit='python3 ${BOLT_SUBMIT_PATH}'
```

## Simcloud Submission

Requires Simcloud cli 04.12.003+
TODO: Installation instructions....

```bash
# UNTESTED
cd simcloud/
./submit.sh
```

## Blobby Sync

If the `BUCKET_PATH` enviornment variable is set, a bucket will be copied from Blobby as part of the setup process (see *util/copy_blobby_bucket*).

**CAUTION:**
Avoid spaces in file names when syncing with Blobby. s3 does not handle them well.

If the `BACKUP_INTERVAL_SEC` enviornment variable is set, the local contents will be synced with the `BUCKET_PATH` at the specified interval via: *util/blobby_sync*

### Bucket Creation

You may create your own bucket to use in blobby. See [Create Bucket Tutorial](https://turiblobby.apple.com/tutorial.html#create-bucket).

**CAUTION: Buckets can not be deleted or renamed!** It is recommended that you use your username to namespace any work:

```bash
USERNAME=$(echo $SC_USERNAME | awk -F: '{print $NF}')
blobby s3api get-bucket-acl --bucket $USERNAME --output text || blobby s3api create-bucket --bucket $USERNAME
```

## Working with Notebooks

The lifetime of the bolt job is tied to the Jupyter server. When you are finished with the job, simply "Quit" the Jupyter server from the notebook Home.
**CAUTION:**
If you are syncing with blobby make sure to run `blobby_sync` before quitting.

If you are having issues with the notebook timing out during a long job, try running the notebook with `jupyter nbconvert`. This will execute the notebook without relying on the browser tab connection and optionally produce an html version when finished.

*execute_notebook* wraps this and saves the partial result if any cell fails. This can be very useful for debugging.

## Docker

### Build a New Image

```bash
cd docker_images/torch_jupyter_py3

IMAGE=<ImageName>:<Tag>
docker build -t $IMAGE .
```

### Run the Image

`docker run -it $IMAGE`

### Test on Simcloud before pushing to Artifactory

`docker save $IMAGE | simcloud bundle upload -`

### Push to Artifactory

```bash
docker tag $IMAGE docker.apple.com/<USER>/$IMAGE
docker push docker.apple.com/<USER>/$IMAGE
```

## Misc Tips

- When debugging bolt configuration, you can save files to BOLT_ARTIFACT_DIR for easy access.

## Resources

[Monitor Running Jobs](https://simcloud-mr2.apple.com/#jobs)

[Docker on Bolt](https://gitlab-turi.corp.apple.com/turi/bolt-sample/tree/master/docker-gpu)

[Docker on Simcloud](https://simcloud.apple.com/tutorials/docker/)

[Docker Images](https://artifacts.apple.com/docker-apple/)

## Inspiration

https://stash.sd.apple.com/projects/ACG/repos/bolt-jupyter/browse

https://github.pie.apple.com/grapaport/fastai-on-bolt

https://stash.sd.apple.com/projects/SIMCLOUD/repos/contrib/browse/course.fast.ai

mail search: turi-bolt-users@group.apple.com notebook

## Remaining Work

- Fix email script - not working within docker container.
- Use S3Zip to reduce start time when copying a bucket (https://turiblobby.apple.com/getting-started.html#install-useful-tools)
- <rdar://problem/46612808> Docker's SHM memory limit is fixed to 64MiB for Docker jobs

Pull requests are welcome!
