import json

def load_dictionary(filename):
	with open(filename, 'r') as file:
		aux = json.load(file)
	return aux