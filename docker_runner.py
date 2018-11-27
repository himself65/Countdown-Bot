#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import docker
import os
import tempfile
import time
import inspect
import ctypes
from threading import Thread
from main import config
from util import print_log


def execute_daemon_calc(callback, container, time_limit, code):
    container.start()
    container.reload()
    begin = time.time()
    timeout = False
    while container.status == "running":
        container.reload()
        import time
        time.sleep(0.1)
        if time.time()-begin > time_limit/1000:
            timeout = True
            break
    if timeout:
        callback("代码'{}'执行超时".format(code))
        return
    output = container.logs().decode("UTF-8")
    container.remove()
    if len(output) > config.OUTPUT_LENGTH_LIMIT:
        output = output[:config.OUTPUT_LENGTH_LIMIT]+"[超出长度限制部分已截断]"
    callback(output)
    # print("{} = {}".format(expression, output))


def run_python_in_docker(callback, code, time_limit):
    print_log("Running .. '{}'".format(code))
    client = docker.from_env()
    # client = docker.DockerClient(base_url="tcp://192.168.10.134:2375")
    tmp_dir = tempfile.mkdtemp()
    file_name = "temp.py"
    with open(os.path.join(tmp_dir, file_name), "w") as file:
        file.write("{}".format(code))
    print_log("Container created.")
    container = client.containers.create("python", "python /temp/{}".format(
        file_name), tty=True, detach=False,  volumes={tmp_dir: {"bind": "/temp", "mode": "ro"}}, mem_limit="10m", memswap_limit="20m", oom_kill_disable=True, nano_cpus=int(0.1*1/1e-9))
    # container = client.containers.create("python", "uname -a".format(
    #     file_name), tty=True, detach=False)
    thd = Thread(target=execute_daemon_calc, args=(
        callback, container, time_limit, code))
    thd.setDaemon(True)
    thd.start()
