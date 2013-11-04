from lxml import etree
tree = etree.parse('eng-asv_usfx.xml')
nt = etree.Element('usfx')
for i, book in enumerate(tree.xpath('//book')):
	if i < 39:
		continue
	nt.append(book)

with open('eng-nt_usfx.xml', 'wb') as f:
	f.write(etree.tostring(nt))
