from lxml import etree
from pprint import pprint

class Processor(object):
    def __init__(self, fname):
        print fname
        self.tree = etree.parse(fname)
        print self.tree
        self.books = list()
        self.process_book()

    def process_verses(self, chapter):
        verses = list()
        for verse in chapter.findall('VERS'):
            verses.append({'id': verse.get('vnumber'), 'content': verse.text,})

        return verses

    def process_chapters(self, book):
        chapters = list()
        for chapter in book.findall('CHAPTER'):
            chapters.append({
                'number': chapter.get('cnumber'),
                'verses': self.process_verses(chapter)
            })
            
        return chapters

    def process_book(self):
        for book in self.tree.findall('//BIBLEBOOK'):
            self.books.append({
                'name': book.get('bnumber'),
                'chapters': self.process_chapters(book)
                })

if __name__ == '__main__':
    p = Processor('nt_zefania_greek.xml')
    print len(p.books)
    with open('test.txt', 'wb') as f:
        for book in p.books:
            for chapter in book['chapters']:
                for verse in chapter['verses']:
                    s = verse['content']
                    if s:
                        f.write(s.encode('utf-8'))
        