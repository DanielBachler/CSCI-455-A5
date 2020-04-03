import random

class Dialog:   
    # Dictionary of definitions used by the dialog engine instance
    definitions = {}

    # List of main level conversations
    conversations = []

    def __init__(self):
        pass

    def add_definition(self, name, values):
        self.definitions[name] = values

class Conversation:
    # List of child conversation objects
    children = None

    # Type of conversation
    converstation_type = None

    def __init__(self, triggers, answer):
        self.triggers = triggers
        self.answer = answer
    
    #Takes in a list of responses
    # and returns a random choice.   
    def randomResponse(self, response_list):
        return random.choice(response_list)