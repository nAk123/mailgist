import nltk
import re
from nltk.probability import *
from lxml import etree

doc = etree.parse('bc3corpus.1.0/annotation.xml')
thread_dict = {}
names = []
for thread in doc.xpath('//thread'):
    for name in thread.xpath('name'):
        thread_dict[name.text] = {}
        names.append(name.text)
        for desc in thread.xpath('annotation/desc'):
            thread_dict[name.text].setdefault(desc.text, [])
            for t in thread.xpath('annotation/summary/sent'):
                 thread_dict[name.text][desc.text].append(t.text)
	    #print thread_dict[name.text][desc.text]

subject_map={}
y=0
for name in names:
    y = y+1
    for x in thread_dict[name]:
        try:
            subj_string=','.join(thread_dict[name][x])
	    #print subj_string
        except TypeError:
            print "Exception occured due to {0}".format(thread_dict[name][x])
        #subject_map[x] = subj_string
    try:
        subject_map[name]=''.join(subj_string)
    except TypeError:
        print "Exception occured due to {0}".format(thread_dict[name])

    print "\nBasic analysis for thread number {0}".format(y)
    text1 = subject_map[name]
    #Tokenize text
    tok_text1 = nltk.word_tokenize(text1)
    #Convert the token set to NLP Text
    nlp_text = nltk.Text(tok_text1)
    print "Number of unique words in the input are {0}".format(len(set(nlp_text)))
    #Find the frequency distribution of the text
    fdist_text1 = FreqDist(nlp_text)
    hapax_text = fdist_text1.hapaxes()
    relwords = [w for w in set(hapax_text) if len(w)>2 and w.isalpha()]
    print "The relevant words are (Most stop words removed):"
    print relwords
    #Analyze the frequency of occurence of words
    len_relwords = [len(w) for w in set(relwords)]
    len_dist = FreqDist(len_relwords)
    print "The count of most frequently occuring relevant words lengths are:"
    print len_dist.items()
