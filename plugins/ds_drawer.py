from graphviz import Digraph
from io import BytesIO
from cqhttp import CQHttp
from register import command
import global_vars
import copy
import pdb
import tempfile
import os
config = global_vars.CONFIG[__name__]


def plugin():
    return {
        "author": "officeyutong",
        "version": 1.0,
        "description": "数据结构绘图器"
    }


class SAMNode:
    link = None
    chds = None
    max_len = 0
    right_size = 0
    vtx_id = 0
    node_list = []
    accept = False

    def __str__(self):
        ret = "SAMNode{{ID:{},max_len={},rightsize={},".format(
            self.vtx_id, self.max_len, self.right_size)
        ret += "link={},".format(None if self.link is None else self.link.vtx_id)
        for k, v in self.chds.items():
            ret += "{}->{},".format(k, v.vtx_id)
        return ret+"}}"

    def __repr__(self):
        return self.__str__()

    def __init__(self, node_list, max_len=0):
        self.max_len = max_len
        self.node_list = node_list
        self.node_list.append(self)
        self.vtx_id = len(node_list)
        self.chds = dict()
        self.right_size = 1

    def clone(self):
        cloned = SAMNode(self.node_list, self.max_len)
        cloned.link = self.link
        cloned.chds = copy.copy(self.chds)
        cloned.right_size = 0
        cloned.accept = False
        return cloned


def append(char: str, last: SAMNode, root: SAMNode, suf_id: int)->SAMNode:
    new = SAMNode(root.node_list, last.max_len+1)
    curr = last
    new.accept = suf_id
    while curr and (char not in curr.chds):
        curr.chds[char] = new
        curr = curr.link
    if curr is None:
        new.link = root
    elif curr.chds[char].max_len == curr.max_len+1:
        new.link = curr.chds[char]
    else:
        oldNode: SAMNode = curr.chds[char]
        newNode: SAMNode = oldNode.clone()
        new.link = oldNode.link = newNode
        newNode.max_len = curr.max_len+1
        while curr is not None and curr.chds[char] == oldNode:
            curr.chds[char] = newNode
            curr = curr.link
    return new


def generate_graph(string):
    nodes = []
    root = SAMNode(nodes)
    root.right_size = 0
    last = root
    for idx, x in enumerate(string):
        last = append(x, last, root, idx+1)
    nodes.sort(key=lambda x: x.max_len, reverse=True)
    dot = Digraph(string)
    for x in nodes:
        if x.link is not None:
            x.link.right_size += x.right_size
    nodes.sort(key=lambda x: x.vtx_id)
    for x in nodes:
        label = "{}\nMax={}\nSize={}".format(
            x.vtx_id, x.max_len, x.right_size)
        if x.accept:
            label += "\nAcceptable"
        dot.node(str(x.vtx_id), label)
    for x in nodes:
        for k, v in x.chds.items():
            dot.edge(str(x.vtx_id), str(v.vtx_id), k)
        if x.link is not None:
            dot.edge(str(x.vtx_id), str(x.link.vtx_id), color="red")
    tmpdir = tempfile.gettempdir()
    target = os.path.join(tmpdir, "qwq")
    dot.render(filename=target, format="png")
    buff = BytesIO()
    with open(target+".png", "rb") as file:
        buff.write(file.read())
    # print(buff.getvalue())
    return buff.getbuffer()


@command(name="sam", help="绘制SAM")
def sam(bot: CQHttp, context, args):
    import base64
    if len(args) < 2:
        bot.send(context, "请输入字符串")
        return
    string = args[1]
    if len(string) > config.MAX_STRING_LENGTH:
        bot.send(context, "长度上限为 {} .".format(config.MAX_STRING_LENGTH))
        return
    result = base64.encodebytes(generate_graph(
        string)).decode().replace("\n", "")
    bot.send(context, "[CQ:image,file=base64://{}]".format(result))


if __name__ == "__main__":
    line = input()
    # sam(None, None, ["", line])
