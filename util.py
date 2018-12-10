import datetime
import urllib
import json
import ctypes
import inspect
from io import BytesIO


def print_log(text, log_type=0):
    print("[%s][%s]: %s" % (datetime.datetime.now(), [
          "MESSAGE", "WARNING", "ERROR"][log_type], str(text)))




def get_text_from_url(url: str)->str:
    result = None
    with urllib.request.urlopen(url) as f:
        result = f.read().decode("utf-8")
    return result
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


