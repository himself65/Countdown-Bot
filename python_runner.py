import docker
import os
import tempfile
import time
import inspect
import ctypes
from threading import Thread
from main import config
from util import print_log

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    """强行终止一个线程"""
    _async_raise(thread.ident, SystemExit)


def execute_daemon_calc(callback, container):
    container.start()
    container.reload()
    while container.status == "running":
        container.reload()
    output = container.logs().decode("UTF-8")
    container.remove()
    if len(output) > config.OUTPUT_LENGTH_LIMIT:
        output = output[:config.OUTPUT_LENGTH_LIMIT]+"[超出长度限制部分已截断]"
    callback(output)
    # print("{} = {}".format(expression, output))


def keeper_thread(thread, callback,  container, code):
    time.sleep(config.EXECUTE_TIME_LIMIT/1000)
    try:
        container.reload()
    except Exception as ex:
        print_log(ex)
        return
    print_log("Waiting timed out , status = {}".format(container.status))
    if container.status == "running":
        stop_thread(thread)
        try:
            container.kill()
            container.remove()
        except Exception:
            pass
        callback("代码 '"+code+"' 执行超时.")
        print_log("Killing")


def run_python_in_docker(callback, code):
    client = docker.from_env()
    # client = docker.DockerClient(base_url="tcp://192.168.10.134:2375")
    tmp_dir = tempfile.mkdtemp()
    file_name = "temp.py"
    with open(os.path.join(tmp_dir, file_name), "w") as file:
        file.write("{}".format(code))
    print_log("Container created.")
    container = client.containers.create("python", "python /temp/{}".format(
        file_name), tty=True, detach=False,  volumes={tmp_dir: {"bind": "/temp", "mode": "ro"}})
    # container = client.containers.create("python", "uname -a".format(
    #     file_name), tty=True, detach=False)
    thd = Thread(target=execute_daemon_calc, args=(
        callback, container))
    thd.setDaemon(True)
    thd.start()
    keeper = Thread(target=keeper_thread, args=(
        thd, callback, container, code))
    keeper.setDaemon(True)
    keeper.start()
