from main import *


def run_python_in_docker(code, callback, timeout):
    pass


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


def execute_daemon_calc(bot: CQHttp, context, container):
    container.start()
    container.reload()
    while container.status == "running":
        container.reload()
    output = container.logs().decode("UTF-8")
    container.remove()
    if len(output) > config.OUTPUT_LENGTH_LIMIT:
        output = output[:config.OUTPUT_LENGTH_LIMIT]+"[超出长度限制部分已截断]"
    bot.send(context, output)
    # print("{} = {}".format(expression, output))


def keeper_thread(thread, bot: CQHttp, context, container, code):
    time.sleep(config.OUTPUT_LENGTH_LIMIT/1000)
    container.reload()
    print("Waiting timed out , status = {}".format(container.status))
    if container.status == "running":
        stop_thread(thread)
        try:
            container.kill()
            container.remove()
        except Exception:
            pass
        bot.send(context, "代码 '"+code+"' 执行超时.")
        print("Killing")


def execute_calc(bot: CQHttp, context, code):
    client = docker.from_env()
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
    file_name = "{}-temp.py".format(int(time.time()))
    with open("/tmp/{}".format(file_name), "w") as file:
        file.write("{}".format(code))
    container = client.containers.create("python", "python /temp/{}".format(
        file_name), tty=True, detach=False,  volumes={"/tmp": {"bind": "/temp", "mode": "ro"}})
    thd = Thread(target=execute_daemon_calc, args=(
        bot, context,  container))
    thd.setDaemon(True)
    thd.start()
    keeper = Thread(target=keeper_thread, args=(
        thd, bot, context, container, code))
    keeper.setDaemon(True)
    keeper.start()
