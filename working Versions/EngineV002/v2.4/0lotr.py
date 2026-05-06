import json

dict_inputMapping = {"artisanship": ["artisanship", "a"]}

def inputMapping():
    user_input = input("enter some text: ")
    for key_name, list_synonyms in dict_inputMapping.items():
        for synonym in list_synonyms:
            if user_input.lower() in list_synonyms:
                print(f"user_input match: '{user_input}' found in list_synomys for '{key_name}'")
                return(key_name)
                
                
inputMapping()