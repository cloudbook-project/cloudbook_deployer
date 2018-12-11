import json, ast

def load_dictionary(filename, configuration = None):
	with open(filename, 'r') as file:
		aux = json.load(file)
	return aux

def load_cloudbook(filename, configuration = None):
	with open(filename, "r") as file:
		txt = str(file.read())
		aux = dict(ast.literal_eval(txt))
		return aux