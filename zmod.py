class Action:
    def __init__(self, name):
        self.name = name
        self.instructions = []
        self.actions = {}
        self.context = {}
        
    def call(self, context):
        return self.instructions + ["_back"]
        
class Context:
    INSTRUCTIONS = "__instructions"
    STACK = "__stack"
    ACTIONS = "__actions"
    
    def __init__(self, main):
        self.data = dict()
        self.data[self.INSTRUCTIONS] = ["main"]
        self.data[self.STACK] = []
        self.data[self.ACTIONS] = {"main": main}
        
    def pushStack(self, action):
        if action is None:
            return
        self.data[self.STACK].append(action)
    
    def peekStack(self):
        return self.data[self.STACK][-1]

    def popStack(self):
        action = self.data[self.STACK][-1]
        self.data[self.STACK] = self.data[self.STACK][:-1]
        return action
        
    def peekInstruction(self):
        return self.data[self.INSTRUCTIONS][0]
    
    def popInstruction(self):
        inst = self.data[self.INSTRUCTIONS][0]
        self.data[self.INSTRUCTIONS] = self.data[self.INSTRUCTIONS][1:]
        return inst
        
    def pushInstructions(self, instructions):
        if instructions is None:
            return
        self.data[self.INSTRUCTIONS] = instructions + self.data[self.INSTRUCTIONS]
        
    def addAction(self, name, action):
        self.data[self.ACTIONS][name] = action
        
    def getAction(self, name):
        if name == "_this":
            return self.data[self.STACK][-1]
        for entry in self.data[self.STACK][::-1]:
            if name in entry.actions:
                return entry.actions[name]
        if name in self.data[self.ACTIONS]:
            return self.data[self.ACTIONS][name]
        return None
    
    def setData(self, name, value):
        for entry in self.data[self.STACK][::-1]:
            if name in entry.context:
                entry.context[name] = value
                return
        if name in self.data:
            self.data[name] = value
            return
        raise KeyError(name)
    
    def getData(self, name):
        for entry in self.data[self.STACK][::-1]:
            if name in entry.context:
                return entry.context[name]
        if name in self.data:
            return self.data[name]
        return None
    
