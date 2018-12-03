from global_vars import registered_commands, message_listeners
import pdb

def command(name, help=""):
    def inner(func):
        registered_commands[name] = (help, func)
    return inner


def message_listener(func):
    message_listeners.append(func)

    def inner():
        return func()
    return inner
