import datetime
import urllib
import json
import ctypes
import inspect
from io import BytesIO


def print_log(text, log_type=0):
    print("[%s][%s]: %s" % (datetime.datetime.now(), [
          "MESSAGE", "WARNING", "ERROR"][log_type], str(text)))


def get_countdown_list(url):
    decoder = json.JSONDecoder()
    result = None
    with urllib.request.urlopen(url) as f:
        result = decoder.decode(f.read().decode("utf-8"))
    return result


def get_text_from_url(url: str)->str:
    result = None
    with urllib.request.urlopen(url) as f:
        result = f.read().decode("utf-8")
    return result


def get_hitokoto():
    import urllib3
    import json
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    response = http.urlopen(url="https://v1.hitokoto.cn/", method="GET")
    data = json.JSONDecoder().decode(response.data.decode())
    response.close()
    to_send =\
        """{text}
            
--- {source}
    
(Hitokoto ID:{id})""".format(text=data["hitokoto"], source=data["from"], id=data["id"])
    return to_send


def get_hitokoto_groups(url):
    broadcast_list = url
    if type(broadcast_list) is str:
        import json
        import util
        broadcast_list = json.JSONDecoder().decode(
            util.get_text_from_url(broadcast_list))
    return broadcast_list


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

# 渲染Latex


def renderLatex(formula: str)->BytesIO:
    from sympy import preview
    print_log("Rendering {}".format(formula))
    buffer = BytesIO()
    preview(formula, viewer="BytesIO", euler=False, outputbuffer=buffer)
    return buffer
