#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2022-2023 All rights reserved.
# FILENAME:    ~~/src/commands/__init__.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-12-01 05:31
# AUTHOR: 	   Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Local modules ###
from src.commands.clean import clean
from src.commands.cluster import cluster
from src.commands.mine import mine
from src.commands.nodekeys import nodekeys
from src.commands.ping_pong import ping_pong
from src.commands.remove_deprecated import remove_deprecated
from src.commands.setup import setup

__all__ = ["clean", "cluster", "mine", "nodekeys", "ping_pong", "remove_deprecated", "setup"]
