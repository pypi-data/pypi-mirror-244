#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/setup.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-12-01 06:18
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Set

### Third-party packages ###
from click import command
from docker import DockerClient, from_env
from rich.progress import track

### Local modules ###
from src.configs import IMAGES


@command
def setup() -> None:
    """Download docker images used by command-line interface."""
    client: DockerClient = from_env()
    if client.ping():
        docker_images: Set[str] = {image.tags[0] for image in client.images.list()}
        for registry_id in track(IMAGES.values(), description="Download required images..."):
            if registry_id in docker_images:
                print(f"<Image: '{ registry_id }'> already exists in local docker images.")
            else:
                repository, tag = registry_id.split(":")
                client.images.pull(repository=repository, tag=tag)
                print(f"<Image: '{ registry_id }'> downloaded.")
    else:
        print("!! Unable to connect to docker daemon.")


__all__ = ["setup"]
