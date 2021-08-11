import json
from bs4 import BeautifulSoup

config_remove_prefix = True # remove words that don't start with alphabet . e.g. suffixes (-ing in i, -s in s)
config_all_lowercase = True # make all words lowercase (not their definitions)
config_only_alpha = False # words consisting of only alphabets allowed. e.g. removes words having spaces or dashes etc.

config_remove_orphans = True # remove words without definition
all_words = []


def gcide_xml2json(file, letter):
	with open(file, 'r') as xml:
		data = xml.read()
		soup = BeautifulSoup(data, 'lxml')
		dic = {}
		word = ''
		words = []
		pos = ''

		for entry_block in soup('p'):
			if entry_block.ent is not None:
				checks = [
					config_remove_prefix and not word.lower().startswith(letter),
					# config_remove_orphans and word != '' and len(dic[word][0].data) == 0,
					config_only_alpha and not word.isalpha()
				]

				delete_entry = any(checks)

				if delete_entry:
					for unwanted_word in words:
						if unwanted_word in dic: del dic[unwanted_word] # band age and Band Age .. same when lowercase

				words = [entry_word.get_text().lower() if config_all_lowercase else entry_word.get_text() for entry_word in entry_block.find_all('ent')]
				word = words[-1] # Root word
				all_words.append(word)
				# entry_words = [entry_word for entry_word in entry_words[:-1] if entry_word[0].isalpha()] + word # remove suffixes

				if entry_block.pos is not None:
					pos = entry_block.pos.get_text()
				else:
					pos = ''

				if word not in dic:
					dic[word] = [
						{
							'pos': pos,
							'data': []
						}
					]
				else:
					for data in dic[word]:
						if data['pos'] != pos:
							dic[word].append(
								{
									'pos': pos,
									'data': []
								}
							)
			
			if word == '':
				continue

			def_entry = entry_block.find('def')
			if def_entry is not None:
				sentences = []
				sentence_entry = def_entry.find('as')
				if sentence_entry != None:
					sentences = sentence_entry.get_text()[4:].split('; ') # Remove "as, " that starts the example sentence
					sentence_entry.clear()

				definitions = def_entry.get_text().strip(' ;.')

				for word_data in dic[word]:
					if word_data['pos'] == pos and len(definitions) != 0:
						word_data['data'].append({
							'definitions': definitions,
							'sentences': sentences
						})

		return dic


if __name__ == '__main__':
	a2z = 'abcdefghijklmnopqrstuvwxyz'
	chapters = {}
	for letter in a2z:
		gcide_xml = 'xml_files/gcide_' + letter + '.xml'
		print('Parsing gcide_%s.xml file...' % (letter))
		chapters[letter] = gcide_xml2json(gcide_xml, letter)

	dictionary = {}
	for letter in chapters:
		dictionary.update(chapters[letter])

	print('Writing dictionary.json and words.txt')
	with open('dictionary.json', 'w', encoding='utf-8') as dictionary_file, open('words.txt', 'w', encoding='utf-8') as words:
		json.dump(dictionary, dictionary_file, indent = True, ensure_ascii=True, sort_keys=True)
		words.write("\n".join(all_words))
