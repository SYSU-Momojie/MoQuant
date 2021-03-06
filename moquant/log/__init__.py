#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Log util """
import codecs
import logging
import sys

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

log_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
level = logging.INFO
stdout = logging.StreamHandler(sys.stdout)
logging.basicConfig(format=log_formatter, level=level, handlers=[stdout])


def get_logger(name: str):
    return logging.getLogger(name)
