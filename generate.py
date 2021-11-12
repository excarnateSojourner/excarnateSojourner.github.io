import os
import re
import sys

TEMPLATE_DIR = 'templates'
CONTENT_DIR = 'content'
SERVED_DIR = 'served'

def main():
	for file_ in os.listdir(CONTENT_DIR):
		if file_.endswith('.xml'):
			print(f'processing {file_}')
			pageData = parseXml(f'{CONTENT_DIR}/{file_}')
			if 'template' not in pageData:
				print(f'Error: `{file_}` does not specify a template to use.', file=sys.stderr)
				continue
			with open(f'{TEMPLATE_DIR}/{pageData["template"]}.html') as templateFile:
				with open(f'{SERVED_DIR}/{file_[:-4]}.html', 'w') as constructedFile:
					try:
						constructedFile.write(templateFile.read().format(**pageData))
					except KeyError as err:
						print(f'Error: `{file_}` does not define `{err.args[0]}`, but it is referenced in the template `{pageData["template"]}`.', file=sys.stderr)

def parseXml(filepath):
	'''Not at all a full XML parser. Just converts the top level of tags into a dict: `<title>foo</title>` becomes `title: 'foo'`.'''
	with open(filepath) as xmlFile:
		dataPairs = re.findall(r'<(\w*)>(.*?)</\1>', xmlFile.read(), re.DOTALL)
	return dict(dataPairs)

if __name__ == '__main__':
	main()
