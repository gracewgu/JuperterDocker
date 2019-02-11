#!/usr/bin/env python3
import os
import tempfile
import shutil
from distutils.dir_util import copy_tree
import yaml
import argparse
import ast
from pathlib import Path

# Pip installs
import turibolt as bolt # pip install --upgrade turibolt --index https://pypi.apple.com/simple

# DEFAULTS
SAVED_CONFIG='/tmp/last_config.yaml'

def replace_value(config, key):
    # Recurse through nested dictionaries.
    if isinstance(config[key], dict):
        print(f'{key}:')
        for nested_key in sorted(config[key].keys()):
            print('\r   ', end='')
            replace_value(config[key], nested_key)
        return

    new_value = input(f'{key}: {config[key]} -> ').strip()
    if new_value == 'd':
        del config[key]
    elif new_value:
        config[key] = type_value(new_value, config[key])


def type_value(new_value, old_value):
    assert isinstance(new_value, str)
    if isinstance(old_value, str): return new_value

    # Evaluating from the ast allows new_value to be encoded as the correct type.
    # https://docs.python.org/3/library/ast.html#ast.literal_eval
    return ast.literal_eval(new_value)


def update_config(config, verbose=False, force=False):
    if verbose:
        print("** Enter new value (d - delete, enter - confirm) **")
        for key in sorted(config.keys()):
            replace_value(config, key)

    print('-'*20)
    print(yaml.dump(config, default_flow_style=False))
    if not force and input("Confirm config (y): ") != 'y':
        # Take a second pass at the config.
        update_config(config, verbose=True)

    return config


def package_with_utils(src, dest:Path):
    """
    Copies the util/ directory in with the submitted src.
    """
    copy_tree(str(src), str(dest)) # Copy even though the destination exists.
    script_path = Path(os.path.realpath(__file__)).parent
    if (dest/'util').exists():
        print("Not copying util/ - directory already exists at", src)
    else:
        shutil.copytree(script_path/'util', dest/'util')


def input_parser():
    """
    Configures the command input.
    :rtype: ArgParser
    """
    parser = argparse.ArgumentParser(description='Submits a Bolt job.')
    parser.add_argument('-v', '--verbose', help="confirm every action", action="store_true")
    parser.add_argument('-f', '--force', help="skip final confirmation", action="store_true")
    parser.add_argument('-r', '--retry', help="retry last config", action="store_true")

    parser.add_argument('--name', help="The name of the job")
    parser.add_argument('--description', help="The description of the job")
    parser.add_argument('-i', '--interactive', help="run an interactive bolt job", action="store_true")
    parser.add_argument('-t', '--tags', help="comma separated list of tags")
    parser.add_argument('-c', '--config', help="path to custom config.yaml file")
    parser.add_argument('-d', '--docker_image', help='Docker image, (You should use the sha, `docker images --digests`) e.g. docker.apple.com/mdewitt/torch_jupyter_py3@sha256:b8ef19bf87785162593ab1436210d051617f71aa271ec67a0c58f957a2ec5b43')
    return parser


def simcloud_good_citizen_reminder():
    CRED = '\033[91m'
    CEND = '\033[0m'
    return f"{CRED}Please be a responsible simcloud citizen and quit the notebook server when finished to free resources for others.{CEND}"


def main():
    args = input_parser().parse_args()

    if args.retry and os.path.exists(SAVED_CONFIG):
        print("Loading saved config:", SAVED_CONFIG)
        config_path = SAVED_CONFIG
    else:
        config_path = args.config or './config.yaml'

    with open(config_path) as f:
        config = yaml.load(f)

    if args.name:
        config['name'] = args.name
    if args.description:
        config['description'] = args.description
    if args.tags:
        config['tags'] = [tag.strip() for tag in args.tags.split(',')]

    if args.docker_image:
        config['resources']['docker_image'] = args.docker_image

    new_config = update_config(config, args.verbose, args.force)
    with open(SAVED_CONFIG, 'w') as f:
        yaml.dump(new_config, f, default_flow_style=False)

    # Create submission which includes utils.
    tmpdir = tempfile.TemporaryDirectory()
    job_dir = Path(tmpdir.name)
    package_with_utils(src='.', dest=job_dir)

    task_info = bolt.submit(new_config, tar=str(job_dir), interactive=args.interactive, exclude=['submit.py'])
    print(simcloud_good_citizen_reminder())


if __name__ == '__main__':
    main()
