import json

def load_dictionary(filename, configuration = None):
	with open(filename, 'r') as file:
		aux = json.load(file)
	return aux