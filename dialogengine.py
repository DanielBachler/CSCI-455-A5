import objects
import shlex
import random

def read_dialog_file(input):
    # Open file
    dialog_file = open(input, 'r')
    # Create dialog object
    dialog = objects.Dialog()
    # Tracker for last first level dialog
    last_first_level = None

    for line in dialog_file:
        line = line.lower()
        # If line is comment ignore
        if line[0] != "#":
            # Determine if definition 
            if line[0] == '~':
                # Split on the space
                defin = line.split(":")
                # Get out name and clean
                name = defin[0]
                name = name[1:]
                name = name.strip()

                # Get out values and clean
                values = bracket_split(defin[1])
                dialog.add_definition(name, values)

                #print(name, values)
            # Determine if First level dialog
            if line[0] == 'u':
                # Get the line in its parts
                converstation = line.split(":")
                # Get out the triggers and clean
                triggers = converstation[1]
                triggers = triggers.strip()
                # Get out the answer and clean
                answer = converstation[2]
                answer = answer.strip()

                # Check if either trigger or answer has brackets and get out values if so
                if '[' in triggers:
                    triggers = bracket_split(triggers)
                if '[' in answer:
                    answer = bracket_split(answer)
                
                # See if a definition is used as a trigger or answer
                if '~' in triggers:
                    triggers = dialog.definitions[triggers[2:len(triggers)-1]]
                if '~' in answer:
                    answer = dialog.definitions[answer[1:]]

                convo = objects.Conversation(triggers, answer)
                dialog.conversations.append(convo)
                last_first_level = convo
            
            # Determine if lower level dialog
            if line[0] == "\t":
                print(line.strip())

            # Check if proposal 
            if line[0] == '&':
                # Idk man
                pass

    return dialog
                
# Takes in a string with the general format ["item string" item2 item3]
#  and returns the values as a list ex. [item string, item2, item3]
def bracket_split(bracket):
    bracket = bracket.replace('[', '')
    bracket = bracket.replace(']', '')
    output_list = [] # Add object list to memory.
    output_list = shlex.split(bracket)
    return output_list

read_dialog_file("sampledialog.txt")