import datetime
import urllib
import json

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