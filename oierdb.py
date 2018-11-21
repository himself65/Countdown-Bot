#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from urllib.request import urlopen
# from bs4 import BeautifulSoup
import urllib
import json


def fetch(name: str):
    decoder = json.JSONDecoder()
    result = None
    with urllib.request.urlopen("http://bytew.net/OIer/search.php?method=normal&q="+urllib.parse.quote(name)) as page:
        result = decoder.decode(page.read().decode("utf-8"))
    return result["result"]


