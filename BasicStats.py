import nltk
import re
from nltk.probability import *
from lxml import etree

def read_xml():
    thread_dict = {}
    s_features = {}
    doc = etree.parse('bc3corpus.1.0/corpus.xml')
    for thread in doc.xpath('//thread'):
        for name in thread.xpath('name'):
            l = 0
            n = name.text
            thread_dict[n] = {}
            s_features[n] = {}
            #names.append(name.text)
            for docs in thread.xpath('DOC'):
                for subject in docs.xpath('Subject'):
                    thread_dict[n].setdefault(subject.text, [])
                    #for Recv in docs.xpath('From'):
                    #    thread_dict[n][subject.text].append(Recv.text)
                    #for to in docs.xpath('To'):
                    #    thread_dict[n][subject.text].append(to.text)
                    for t in docs.xpath('Text/Sent'):
                        s = t.text
                        thread_dict[n][subject.text].append(s)
                        s_features[n][s] = []
                        #Feature in the 0th column is thread_line_num
                        s_features[n][s].append(l)
                        #1st column feature - t_rel_pos
                        s_features[n][s].append(len(s))
                        #2nd column conatins is Question
                        if '?' in s:
                            s_features[n][s].append(1)
                        else:
                            s_features[n][s].append(0)
                        l += 1
                    print thread_dict[name.text][subject.text]
            #s_features[name.text] = basic
            print "The basic feature set is {0}".format(s_features[n])
            count = l
            print "The total number of sentences are"
            print count
            print "\n"
    return thread_dict, s_features, count

def print_Stats(t_dict):
    subject_map = {}
    y = 0
    for name in t_dict:
        y += 1
        for x in t_dict[name]:
            try:
                subj_string=','.join(t_dict[name][x])
            except TypeError:
                print "Exception occured due to {0}".format(t_dict[name][x])
            #subject_map[x] = subj_string
        try:
            subject_map[name]=''.join(subj_string)
        except TypeError:
            print "Exception occured due to {0}".format(t_dict[name])

        print "The total content of thread number {0} is".format(y)
        print subject_map[name]
        print "\nBasic analysis for thread number {0}".format(y)
        text1 = subject_map[name]
        #Tokenize text
        tok_text1 = nltk.word_tokenize(text1)
        print "The tokenized text is {0}".format(tok_text1)
        #Convert the token set to NLP Text
        nlp_text = nltk.Text(tok_text1)
        #print nlp_text.concordance('severe')
        #print nlp_text.similar('useful')
        #print nlp_text.common_contexts(["useful","very"])
        #Print the nltk generated abstract
        print "The nltk generated abstract is"
        print nlp_text.generate()
        print "Number of words in the input are {0}".format(len(nlp_text))
        print "Number of unique words in the input are {0}".format(len(set(nlp_text)))
        #Find the frequency distribution of the text
        fdist_text1 = FreqDist(nlp_text)
        vocab_text1 = fdist_text1.keys()
        print "The hapaxes in the given text are {0}".format(fdist_text1.hapaxes())
        #fdist_text1.plot(20, cumulative=True)
        #Find the basic set of relevant words
        relwords = [w for w in set(nlp_text) if len(w)>2 and w.isalpha()]
        print "The relevant words are (Most stop words removed):"
        print relwords
        print "The number of relevant words are {0}".format(len(relwords))
        #Analyze the frequency of occurence of words
        len_relwords = [len(w) for w in set(relwords)]
        len_dist = FreqDist(len_relwords)
        print "The count of most frequently occuring relevant words lenths are:"
        print len_dist.items()
        #fdist_text1.plot(40, cumulative=True)
