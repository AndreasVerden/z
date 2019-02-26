import shlex
from zmod import *


class ReadAction(Action):
    """READ"""
    def __init__(self):
        super(ReadAction, self).__init__("system::read")
        
    def call(self, context):
        raw_in = input("> ")
        prc_in = shlex.split(raw_in)
        
        dest = context.popInstruction()
        if dest == "_default":
            return ["_back"] + prc_in
        context.data[dest] = prc_in
        return ["_back"]

class WriteAction(Action):
    """WRITE"""
    def __init__(self):
        super(WriteAction, self).__init__("system::write")
        
    def call(self, context):
        out = context.popInstruction()
        if out == "$":
            out = context.getData(context.popInstruction())
        print(out)
        return ["_back"]
    
class ErrorAction(Action):
    """WRITE"""
    def __init__(self):
        super(ErrorAction, self).__init__("system::error")
        
    def call(self, context):
        out = context.popInstruction()
        print("[ERR]", out)
        return ["_exit"]
