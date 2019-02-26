import sys
from zmod import *


class HelpAction(Action):
    """HELP"""
    def __init__(self):
        super(HelpAction, self).__init__("system::help")
    
    def call(self, context):
        options = context.data[context.STACK][-2].actions.keys()
        print("options:")
        for option in options:
            if option.startswith("_") and context.data["_debug"] == "false":
                continue
            print (" * ", option)
        print("")
        return ["_back"]
    
class CheckAction(Action):
    """CHECK"""
    def __init__(self):
        super(CheckAction, self).__init__("system::check")
        
    def call(self, context):
        check_type = context.popInstruction()
        variable = context.popInstruction()
        data = context.getData(variable)
        value = context.popInstruction()
        
        print(check_type)
        print(variable)
        print(data)
        print(value)
        
        
        success_actions = list()
        for action in range(int(context.popInstruction())):
            success_actions.append(context.popInstruction())

        failed_actions = list()
        for action in range(int(context.popInstruction())):
            failed_actions.append(context.popInstruction())
            
        if data is None:
            return ["_error", "{0} undefined".format(variable)]
        
        if check_type == "contains":
            if value not in data:
                return ["_back"] + failed_actions
            else:
                return ["_back"] + success_actions
        
        if check_type == "equals":
            if data == value:
                return ["_back"] + success_actions
            else:
                return ["_back"] + failed_actions

class DataAction(Action):
    """DATA"""
    def __init__(self):
        super(DataAction, self).__init__("system::data")
        
    def call(self, context):
        action_type = context.popInstruction()
        if action_type == "set":
            key = context.popInstruction()
            value = context.popInstruction()
            
            try:
                context.setData(key, value)
            except KeyError:
                return ["_error", "{0} undefined".format(key)]
                
        
        if action_type == "append":
            key = context.popInstruction()
            value = context.popInstruction()
            
            var = context.getData(key)
            if var is None:
                return ["_error", "{0} undefined".format(key)]
            
            var.append(value)
            
        if action_type == "list":
            print("keys:")
            for key in context.data.keys():
                print(" * ", key)
        
        return ["_back"] 
class ExitAction(Action):
    """EXIT"""
    def __init__(self):
        super(ExitAction, self).__init__("system::exit")
        
    def call(self, context):
        sys.exit(0)

class BackAction(Action):
    """BACK"""
    def __init__(self):
        super(BackAction, self).__init__("system::back")
        
    def call(self, context):
        context.popStack()
        context.popStack()

