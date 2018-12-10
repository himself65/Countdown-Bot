from register import command
from cqhttp import CQHttp


def plugin():
    return {
        "author": "officeyutong",
        "version": 1.0,
        "description": "喵呜"
    }


@command(name="吸猫", help="吸猫")
def suck_cats(bot: CQHttp, context, args):
    """
    ???
    """
    bot.send(context, "喵呜~")
