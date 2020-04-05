import random

class Dialog:   
    # Dictionary of definitions used by the dialog engine instance
    definitions = {}

    # List of main level conversations
    conversations = []

    # Proposal (only one, if one already throw error)
    proposal = None

    proposal_responses = []

    # State for if adding to proposal
    add_to_proposal = False

    def __init__(self):
        self.definitions = {}
        self.conversations = []
        self.proposal = None
        self.proposal_responses = []
        self.add_to_proposal = False

    def add_definition(self, name, values):
        self.definitions[name] = values

    # Debug function for checking tree correctness 
    def printDialog(self):      
        # Recursive function to print any and all paths in the dialog tree.     
        def printNode(node):
            # Tabs for formatting in the dubug function.
            tabs = ""
            for i in range(node.level):
                tabs += "\t"
            print("%s%s: %s" % (tabs, node.triggers, node.answer))
            #if the node has children, call the function again.
            if(node.children is not None):
                for j in node.children:
                    printNode(j)  
        # If a proposal exists print itself and children.               
        if self.proposal is not None:
            print(self.proposal)
            for child in self.proposal_responses:
                printNode(child)      
        for i in self.conversations:
            printNode(i)
         

class Conversation:
    # List of child conversation objects
    children = []

    # Type of conversation
    level = None

    def __init__(self, triggers, answer, level):
        self.triggers = triggers
        self.answer = answer
        self.level = level
        self.children = []
    
    #Takes in a list of responses
    # and returns a random choice.   
    def randomResponse(self):
        return random.choice(self.answer)