from lxml import etree
doc = etree.parse('bc3corpus.1.0/corpus.xml')
#names = [x.text for x in doc.xpath('//thread/name')]
#print names

#subject = [x.text for x in doc.xpath('//thread/DOC/Subject')]
#print subject
#thread in doc.xpath('//threads'): [...] for docs in thread.xpath('/DOC')

count=0
thread={}
for Thread in doc.xpath('//thread'):
	for name in Thread.xpath('name'):
        	thread[name.text]={}
		for docs in Thread.xpath('DOC'):
        		for subject in docs.xpath('Subject'):
                		thread[name.text][subject.text]=[]
        			for Recv in docs.xpath('From'):
                			thread[name.text][subject.text]=[Recv.text]
        			for to in docs.xpath('To'):
					thread[name.text][subject.text].append(to.text)
        			for t in docs.xpath('Text/Sent'):
                			thread[name.text][subject.text].append(t.text)

print thread
