from __future__ import division
import BasicStats as bs

'''
The structure of the sentence feature set basic is as follows
[t_line_num, length, isQuestion, t_rel_pos]
'''

def s_extractor(s_features, count):
    for name in s_features:
        for s in s_features[name]:
            l = s_features[name][s][0]
            s_features[name][s].append(l/count)
    print s_features

def main():
    thread_dict, s_features, count = bs.read_xml()
    #bs.print_Stats(thread_dict)
    print "Entering the sentence extractor"
    s_extractor(s_features, count)

if __name__ == '__main__':
    main()
