import os
import re
import sys

TEMPLATE_DIR = 'templates'
CONTENT_DIR = 'raw'
SERVED_DIR = 'e'

def main():
	'''Fill in templates with page content and other parameters.
	I did try (22-09) to use Python's real XML parsing here, but I found it did not work well at all because HTML is not really a subset of XML. In particular:
	* Attributes need to have values (and allowfullscreen in YouTube embeds does not).
	* All ampersands need to be escaped, even in quoted attribute values.
	* Other escapes like &nbsp; can*not* be used.'''

	for file_ in os.listdir(CONTENT_DIR):
		if file_.endswith('.xml'):
			print(f'processing {file_}')
			pageData = parseXml(f'{CONTENT_DIR}/{file_}')
			if 'template' not in pageData:
				print(f'Error: `{file_}` does not specify a template to use.', file=sys.stderr)
				continue
			pageData['main'] = re.sub(r" href='https?://.*?'", r"\g<0> target='_blank'", pageData['main'])

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
