from cqhttp import CQHttp
from util import print_log
from register import command
from global_vars import registered_commands as commands
from global_vars import config
import re
import util
import sympy
import threading
import time
import base64
from io import BytesIO


def plugin():
    return {
        "author": "officeyutong",
        "version": 1.0,
        "description": "数学积分和Latex渲染支持."
    }


@command(name="integrate", help="对f(x)进行不定积分")
def integrate(bot: CQHttp, context=None, args=None):

    def process():
        func = "".join(map(lambda x: x+" ", args[1:]))
        x = sympy.symbols("x")
        print_log("Integrate for "+func)

        def integrate():
            print_log("Starting...")
            try:
                res = sympy.integrate(func, x)
                buffer: BytesIO = renderLatex(
                    "$${}$$".format(sympy.latex(res)))
                bot.send(context, "Python表达式:\n{}\n\nLatex:\n{}\n\n图像:\n[CQ:image,file=base64://{}]".format(
                    res, sympy.latex(res), base64.encodebytes(buffer.getvalue()).decode(
                        "utf-8").replace("\n", "")))
            except Exception as ex:
                bot.send(context, ("{}".format(ex))[:300])
                raise ex
            print_log("Done...")
        thd2 = threading.Thread(target=integrate)
        thd2.start()
        begin = time.time()
        while time.time()-begin < 5:
            time.sleep(0.1)
        if thd2.is_alive():
            bot.send(context, "积分{}运行超时.".format(func))
            util.stop_thread(thd2)

    thread = threading.Thread(target=process)
    thread.start()


@command(name="latex", help="渲染Latex公式")
def renderlatex(bot: CQHttp, context=None, args=None)->None:
    from io import BytesIO
    import base64
    formula = "".join(map(lambda x: x+" ", args[1:]))
    try:
        buffer: BytesIO = renderLatex(formula)
        bot.send(context, "[CQ:image,file=base64://{}]".format(
            base64.encodebytes(buffer.getvalue()).decode(
                "utf-8").replace("\n", "")
        ))
    except Exception as ex:
        bot.send(context, "渲染Latex时发生错误:\n{}".format(ex))


def renderLatex(formula: str)->BytesIO:
    from sympy import preview
    print_log("Rendering {}".format(formula))
    buffer = BytesIO()
    preview(formula, viewer="BytesIO", euler=False, outputbuffer=buffer)
    return buffer
