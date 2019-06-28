import json

with open('json_example.json') as json_file:  
    data = json.load(json_file)
    print(data)
    print()

    for key, val in data.items():
    	print("{}: {}".format(key, val))