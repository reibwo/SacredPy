from lxml import etree
from pprint import pprint
import json

ons = {'o': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}


class Processor(object):
    book_id = 0
    chapter_id = 0
    verse_id = 0
    
    def __init__(self, fname):
        self.tree = etree.parse(fname)
        self.books = list()
        self.chapters = list()
        self.verses = list()

        self.process_book()
        
    def process_verses(self, chapter):
        verse_number = 0
        for verse in chapter.findall('o:verse', namespaces=ons):
            self.verse_id += 1
            verse_number += 1
            self.verses.append({
                'pk': self.verse_id,
                'fields': {
                    'chapter_id': self.chapter_id,
                    'verse_no': verse_number,
                    'title': verse.get('osisID'), 
                    'content': verse.text,
                    },
                'model': 'askbot.Thread',
            })

    def process_chapters(self, book):
        chapter_number = 0
        for chapter in book.findall('o:chapter', namespaces=ons):
            self.chapter_id += 1
            chapter_number += 1
            self.chapters.append({
                'pk': self.chapter_id,
                'fields': {
                    'book_id': self.book_id,
                    'name': chapter.get('osisID'),
                    'num': chapter_number,
                    'notes': '',
                    },
                'model': 'askbot.Chapter',
            })
            self.process_verses(chapter)

    def process_book(self):
        for book in self.tree.findall('//o:div[@type="book"]', namespaces=ons):
            self.book_id += 1
            self.books.append({
                'pk': self.book_id,
                'fields': {
                    'name': book.get('osisID'),
                    'source_language_id': 1,
                    'notes': '',
                    'edition': '',
                },
                'model': 'askbot.Book',
                })
            self.process_chapters(book)

if __name__ == '__main__':
    p = Processor('nt_zefania_english.xml')
    print len(p.books)
    with open('newtestament.json', 'wb') as f:
        f.write(json.dumps(p.books + p.chapters + p.verses))
    print 'done'

