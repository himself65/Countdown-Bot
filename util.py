import datetime


def print_log(text, log_type=0):
    print("[%s][%s]: %s" % (datetime.datetime.now(), [
          "MESSAGE", "WARNING", "ERROR"][log_type], str(text)))


def get_countdown_list():
    import urllib
    import config
    import json
    decoder = json.JSONDecoder()
    result = None
    with urllib.request.urlopen(config.LIST_URL) as f:
        result = decoder.decode(f.read().decode("utf-8"))
    return result
