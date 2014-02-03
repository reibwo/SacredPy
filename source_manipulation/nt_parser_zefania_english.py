from lxml import etree
from pprint import pprint
import json
import datetime

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
       
    def now(self):
        return str(datetime.datetime.now()).replace(' ','T')
    
    def process_verses(self, chapter):
        verse_number = 0
        for verse in chapter.findall('o:verse', namespaces=ons):
            self.verse_id += 1
            verse_number += 1
            self.verses.append(
                {u'fields': {u'accepted_answer': None,
                             u'added_at': self.now(),
                             u'answer_accepted_at': None,
                             u'answer_count': 0,
                             u'approved': True,
                             u'chapter': self.chapter_id,
                             u'close_reason': None,
                             u'closed': False,
                             u'closed_at': None,
                             u'closed_by': None,
                             u'deleted': False,
                             u'favourite_count': 1,
                             u'followed_by': [],
                             u'language_code': u'en',
                             u'last_activity_at': self.now(),
                             u'last_activity_by': 1,
                             u'points': 0,
                             u'tagnames': u'',
                             u'tags': [],
                             u'title': verse.get('osisID'),
                             u'verse_no': verse_number,
                             u'view_count': 0},
                 u'model': u'askbot.thread',
                 u'pk': self.verse_id},)
            self.verses.append(
            {u'fields': {u'added_at': self.now(),
                         u'approved': True,
                         u'author': 1,
                         u'comment_count': 0,
                         u'deleted': False,
                         u'deleted_at': None,
                         u'deleted_by': None,
                         u'html': verse.text,
                         u'is_anonymous': True,
                         u'language_code': u'en',
                         u'last_edited_at': None,
                         u'last_edited_by': None,
                         u'locked': False,
                         u'locked_at': None,
                         u'locked_by': None,
                         u'offensive_flag_count': 0,
                         u'old_answer_id': None,
                         u'old_comment_id': None,
                         u'old_question_id': None,
                         u'parent': None,
                         u'points': 0,
                         u'post_type': u'question',
                         u'summary': verse.text,
                         u'text': verse.text,
                         u'thread': self.verse_id,
                         u'vote_down_count': 0,
                         u'vote_up_count': 0,
                         u'wiki': False,
                         u'wikified_at': None},
             u'model': u'askbot.post',
             u'pk': self.verse_id},)
            # TODO: perhaps activity, postrevision also?

    def process_chapters(self, book):
        chapter_number = 0
        for chapter in book.findall('o:chapter', namespaces=ons):
            self.chapter_id += 1
            chapter_number += 1
            self.chapters.append({
                'pk': self.chapter_id,
                'fields': {
                    'book': self.book_id,
                    'name': chapter.get('osisID'),
                    'num': chapter_number,
                    'notes': '',
                    },
                'model': 'askbot.chapter',
            })
            self.process_verses(chapter)

    def process_book(self):
        for book in self.tree.findall('//o:div[@type="book"]', namespaces=ons):
            self.book_id += 1
            self.books.append({
                'pk': self.book_id,
                'fields': {
                    'name': book.get('osisID'),
                    'source_language': 1,
                    'notes': '',
                    'edition': '',
                },
                'model': 'askbot.book',
                })
            self.process_chapters(book)

if __name__ == '__main__':
    p = Processor('nt_zefania_english.xml')
    print len(p.books)
    with open('newtestament.json', 'wb') as f:
        f.write(json.dumps(p.books + p.chapters + p.verses))
    print 'done'

