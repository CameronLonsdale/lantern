import re

def remove_punctuation(text, filter='[^A-Za-z]'):
	return re.sub(filter, '', text)
