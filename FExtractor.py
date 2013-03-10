from __future__ import division
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import BasicStats as bs
import nltk

'''
The structure of the sentence feature set basic is as follows
[t_line_num, length, isQuestion, t_rel_pos]

Got a bit of help from Christian S Perone's blog ;)

And sklearn is just amazing - use it!
Combine it with nltk and you have someone you really LOVE.
(or is it someone that really loves YOU)
'''

def s_extractor(s_features, count):
    for name in s_features:
        for s in s_features[name]:
            l = s_features[name][s][0]
            s_features[name][s].append(l/count)
    return s_features

def tfidf_score(train_set, test_set):
    stopwords = nltk.corpus.stopwords.words('english')
    vectorizer = TfidfVectorizer(min_df=1, stop_words=set(stopwords))
    #Remove all the None Types from the input datasets
    train_set = filter(None, train_set)
    test_set = filter(None, test_set)
    vectorizer.fit_transform(train_set)
    print "Word Index is {0} \n".format(vectorizer.vocabulary_)
    smatrix = vectorizer.transform(test_set)
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(smatrix)
    print "IDF scores:", tfidf.idf_
    tf_idf_matrix = tfidf.transform(smatrix)
    msum = tf_idf_matrix.sum(axis=1)
    mlist = msum.tolist()
    count = 0
    tfidfscores = {}
    for s in train_set:
        tfidfscores[s] = mlist[count][0]
        count += 1
    return tfidfscores

def main():
    thread_dict, s_features, count = bs.read_xml()
    #bs.print_Stats(thread_dict)
    s_msgscore = {}
    for name in thread_dict:
        s_msgscore[name] = []
        for subject in thread_dict[name]:
            print "The message being ripped is {0} \n".format(thread_dict[name][subject])
            s_msgscore[name].append(tfidf_score(thread_dict[name][subject], thread_dict[name][subject]))
        print "Sentence score/message is {0} \n".format(s_msgscore[name])
    s_features = s_extractor(s_features, count)

if __name__ == '__main__':
    main()
