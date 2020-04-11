import json
import os


FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/debug_vars"

dict_vars = None
if os.path.isfile(FILE_PATH):
    with open(FILE_PATH) as json_file:
        dict_vars = json.load(json_file)

if __name__ == "__main__":
    print(dict_vars)
