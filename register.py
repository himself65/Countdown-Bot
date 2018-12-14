from global_vars import registered_commands, message_listeners, loop_threads, console_commands
from global_vars import config as global_config

import pdb


def command(name, help=""):
    def inner(func):
        registered_commands[name] = (help, func)
    return inner


def console_command(name, help=""):
    def inner(func):
        console_commands[name] = (help, func)
    return inner


def message_listener(func):
    message_listeners.append(func)

    def inner():
        return func()
    return inner


def schedule_loop(hour, minute, check_interval=global_config.CHECK_INTERVAL, execute_delay=global_config.EXECUTE_DELAY, name="Schedule Loop"):
    from util import print_log
    import time
    import threading
    print_log("Registering schedule loop:%s at %2d:%2d every day." %
              (name, hour, minute))

    def schedule(hour: int, minute: int, check_interval: int, execute_delay: int, todo, name="Schedule Task"):
        while True:
            while True:
                from datetime import datetime
                curr = datetime.now()
                if curr.hour == hour and curr.minute == minute:
                    break
                print_log("Checking '"+name+"'")
                time.sleep(check_interval)
            print_log("Executing '"+name+"'")
            todo()
            time.sleep(execute_delay)

    def inner(func):
        loop_threads.append(threading.Thread(
            target=schedule,
            args=(
                hour, minute, check_interval, execute_delay, func, name
            ),
            name="ScheduleLoop-%s" % name
        ))
    return inner
