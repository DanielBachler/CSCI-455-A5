import dialogengine
def main():
   fileInput = input("Please enter the name of the dialog file: ")
   engine = dialogengine.read_dialog_file(fileInput)
   
main() 