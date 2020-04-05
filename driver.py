import dialogengine

def main():
   engine = None
   while engine is None:
      fileInput = input("Please enter the name of the dialog file: ")
      engine, error = dialogengine.read_dialog_file(fileInput)
      if engine is None and error == 1:
         print("File name is invalid please enter a correct file name\n")
      elif engine is None and error == 2:
         print("There was an error parsing your file human\n")
      elif engine is None and error == 3:
         print("There is a second proposal in your file human, this is illegal\n")
   
   print("Successfully parsed file human")
   print("Enter: 'quit' to exit the program\n-------------\n")
   dialog(engine)
   
   
def dialog(engine):
   userInput = ""
   current_choice_level = []
   if engine.proposal is not None:
      # Print proposal and go from there
      print(engine.proposal)
      current_choice_level = engine.proposal_responses
   else:
      # Get input from user to start
      current_choice_level = engine.conversations
   userInput = input(">").lower()
   while userInput != "quit":
      response_found = False
      # Iterate over conversation objects
      for conversation in current_choice_level:
         # Iterate over triggers in current conversation object (may be 1)
         for trigger in conversation.triggers:
            # If the userinput is a trigger or contains a trigger
            if trigger in userInput:
               response_found = True
               # Print the response (either single or random from list)
               print(conversation.randomResponse())
               # Check if we can go deeper
               if conversation.children != []:
                  current_choice_level = conversation.children
               else:
                  # If we can't, reset conversation level to 0
                  current_choice_level = engine.conversations
      if not response_found:
         print("You didn't enter a valid conversation continuation")
      print("------")
      userInput = input(">").lower()

               
main() 

 # U: => U1 => U2 => U3 => U4 => U5 => U5 => U6 => U6 => U2 => U3 => U1 => #U =>