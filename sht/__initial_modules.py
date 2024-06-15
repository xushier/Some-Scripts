#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import os
import re
import sys
import time
import json
import shutil
import logging
import logging.handlers
from queue import Queue
from datetime import datetime, timedelta
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

import importlib.util
import subprocess

def install_if_needed(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"模块 {module_name} 未安装，正在尝试安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

install_if_needed('requests')
install_if_needed('pymongo')
install_if_needed('clouddrive')
# install_if_needed('grpcio')

import requests
from pymongo import MongoClient, errors
from clouddrive import CloudDriveClient
from CloudDrive_pb2 import AddOfflineFileRequest, FileRequest, OfflineFileListAllRequest
from __notifier import send


