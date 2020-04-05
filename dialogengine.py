import objects
import shlex
import random

def read_dialog_file(input):
    try:
        # Open file
        dialog_file = open(input, 'r')
        # Create dialog object
        dialog = objects.Dialog()
    except IOError as e:
        print("There was an error opening that file. ") 
        return None, 1
    
    try:
        for line in dialog_file:
            line = line.lower()
            # Should make all u's look the same
            line = line.strip()
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
                    parse_u_line(line, dialog)

                # Check if proposal 
                if line[0] == '&':
                    if dialog.proposal is not None:
                        # Second proposal detected
                        return None, 3
                    else:
                        # No other proposal found, assign this as proposal
                        # Get the text to print out of line
                        text = line.split(":")
                        to_print = text[1].strip()
                        dialog.proposal = to_print
                        dialog.add_to_proposal = True
    except IOError as e:
        # There was an error parsing the file.
        return None, 2
    return dialog, 0

# Fix hardcoding of spacing
def parse_u_line(line, dialog):
    # Strip the line of extra spacing
    # line = line.strip()
    # Get level of the line
    level = 0 if line[1] == ":" else int(line[1])
    # Get the line in its parts
    converstation = line.split(":")

    # Get triggers and answer out
    triggers = converstation[1]
    answer = converstation[2]

    # Clean triggers
    triggers = triggers.strip()
    # Remove the parentheses from the triggers
    open = triggers.index("(")
    close = triggers.index(")")
    triggers = triggers[open+1:close]
    triggers = triggers.strip()
    # Clean answer
    answer = answer.strip()

    # See if a definition is used as a trigger or answer
    triggers_def = False
    answer_def = False
    try:
        if '~' in triggers:
            triggers = dialog.definitions[triggers[1:]]
            triggers_def = True
        if '~' in answer:
            answer = dialog.definitions[answer[1:]]
            answer_def = True
    except:
        print("Required definition is not available, check your spelling")

    # Check if either trigger or answer has brackets and get out values if so
    if '[' in triggers:
        triggers = bracket_split(triggers)
    elif triggers_def is False:
        triggers = [triggers]
    if '[' in answer:
        answer = bracket_split(answer)
    elif answer_def is False: 
        answer = [answer]

    # Make the dialog object
    convo = objects.Conversation(triggers, answer, level)

    # Determine where to put dialog object
    if level == 0:
        dialog.conversations.append(convo)
        dialog.add_to_proposal = False
    else:
        if dialog.add_to_proposal:
            if level == 1:
                dialog.proposal_responses.append(convo)
            else:
                last_1_level = dialog.proposal_responses[-1]
                parent_object = last_1_level
                while parent_object.level != level - 1:
                    parent_object = parent_object.children[-1]
                parent_object.children.append(convo)
        else:
            # Find last 0 level dialog object
            last_0_level = dialog.conversations[-1]
            # Set parent object to main level converstation
            parent_object = last_0_level
            # Iterate over last added children through tree 
            #  until a converstation with level = -1 of current convo is found
            while parent_object.level != level - 1:
                parent_object = parent_object.children[-1]
            # Append current converstation to found parent
            parent_object.children.append(convo)

# Takes in a string with the general format ["item string" item2 item3]
#  and returns the values as a list ex. [item string, item2, item3]
def bracket_split(bracket):
    bracket = bracket.replace('[', '')
    bracket = bracket.replace(']', '')
    output_list = [] # Add object list to memory.
    output_list = shlex.split(bracket)
    return output_list

# DEBUG
# dialog, eh = read_dialog_file("sampledialog.txt")
# dialog.printDialog()