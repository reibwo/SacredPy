from lxml import etree
from pprint import pprint

class Processor(object):
	def __init__(self, fname):
		self.tree = etree.parse(fname)
		self.books = list()
		self.process_book()

	def process_chapters(self, book):
		chapters = list()
		for chapter in book.findall('c'):
			current_chapter = {
				'number': chapter.get('id'),
				'verses': list()
			}
			
			for para in chapter.itersiblings():
				if para.tag != 'p':
					continue
				
				for descendant in para.iterdescendants():
					verse_content = ''
					if descendant.tag == 'v':
						verse_number = descendant.get('id')
						verse_content = ((descendant.text or '') + (descendant.tail or '')).strip()
						
						for sibling in descendant.itersiblings():
							verse_content += sibling.text or ''
						current_chapter['verses'].append({'verse_number': verse_number, 
						                          	      'verse_content': verse_content})
			chapters.append(current_chapter)
		return chapters

	def process_book(self):
		for book in self.tree.findall('book'):
			current_book = {
				'name': book.find('h').text.strip(),
				'chapters': self.process_chapters(book)
				}
			self.books.append(current_book)

			
if __name__ == '__main__':
	p = Processor('eng-nt_usfx.xml')
	for book in p.books:
		if book['name'].startswith('Matt'):
			pprint(book)