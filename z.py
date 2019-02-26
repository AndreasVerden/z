# todo
#   recursive actions (scopes)
#   register action action (wtf?)
#   args validation

import sys
import json

from zmod import *
from zio import *
from zstd import *



def deserialize_action(json):
    name = json["name"]
    instructions = json["instructions"]
    
    
    action = Action(name)
    
    action.instructions = instructions
    actions = dict()
    if "actions" in json:
        for entry in json["actions"]:
            child_action = deserialize_action(entry)
            actions[entry["name"]] = child_action
    action.actions = actions
    
    if "context" in json:
        action.context = (json["context"])
    
    return action

# deserialize game from .json
file_name = sys.argv[1]
game = None
with open(file_name) as game_file:
    game = json.load(game_file)
main = deserialize_action(game)

# init context
context = Context(main)

# std
context.addAction("help", HelpAction())
context.addAction("back", BackAction())
context.addAction("_check", CheckAction())
context.addAction("_data", DataAction())
context.addAction("_back", BackAction())
context.addAction("_exit", ExitAction())
context.addAction("_error", ErrorAction())

# io
context.addAction("_read", ReadAction())
context.addAction("_write", WriteAction())


if "debug" in sys.argv: 
    context.data["_debug"] = "true"
else:
    context.data["_debug"] = "false"

def debug_status(context):
    stack = context.data[context.STACK]
    action = context.data[context.STACK][-1]
    insts = context.data[context.INSTRUCTIONS]
    
    print()
    print("# stack:")
    for call in stack:
        print("#\t",call.name)
    print("# action:", action.name)
    print("# insts:", insts)
    print("#", action.name, context.peekInstruction())
    
def debug_actions(context):
        print("# actions")
        for action in context.data[context.ACTIONS]:
            print("#\t", action)

def main():
    if context.data["_debug"] == "true": debug_actions(context)

    while True:        
        instruction_name = context.popInstruction()
        #print("A ", instruction_name)
        new_action = context.getAction(instruction_name)
        if new_action is None:
            print("[WAR] Unknown Instruction")
            continue
        
        #print("B ", new_action, new_action.name)
        context.pushStack(new_action)
        #print("D1 ", context.data[context.INSTRUCTIONS])
        instructions = new_action.call(context)
        #print("C ", instructions)
        #print("D2 ", context.data[context.INSTRUCTIONS])
        if instructions is not None:
            context.pushInstructions(instructions)
            #print("D3 ", context.data[context.INSTRUCTIONS])
        if context.data["_debug"] == "true": debug_status(context)


# start game
main()
