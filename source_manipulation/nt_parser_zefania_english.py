from lxml import etree
from pprint import pprint
ons = {'o': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}

class Processor(object):
    def __init__(self, fname):
        self.tree = etree.parse(fname)
        print self.tree
        self.books = list()
        self.process_book()

    def process_verses(self, chapter):
        verses = list()
        for verse in chapter.findall('o:verse', namespaces=ons):
            verses.append({'id': verse.get('osisID'), 'content': verse.text,})

        return verses

    def process_chapters(self, book):
        chapters = list()
        for chapter in book.findall('o:chapter', namespaces=ons):
            chapters.append({
                'number': chapter.get('osisID'),
                'verses': self.process_verses(chapter)
            })
            
        return chapters

    def process_book(self):
        for book in self.tree.findall('//o:div[@type="book"]', namespaces=ons):
            self.books.append({
                'name': book.get('osisID'),
                'chapters': self.process_chapters(book)
                })

if __name__ == '__main__':
    p = Processor('nt_zefania_english.xml')
    print len(p.books)
    for book in p.books:
        pprint(book)