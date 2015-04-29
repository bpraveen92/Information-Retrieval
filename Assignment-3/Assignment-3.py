
import re
import math
from collections import defaultdict
import nltk.metrics
from copy import deepcopy
import sys
import operator
from matplotlib import pyplot as plt
    
def tokenize(document):
    return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]

def stem(tokens):
    return [re.sub('^(did|does)$', 'do', t) for t in tokens]

def read_timeall():
    return read_delim('TIME.ALL')

def read_timeque():
    return read_delim('TIME.QUE')

def read_timerel():
    #return [l.strip() for l in open(filename, 'rt').readlines()]
    result = defaultdict()
    infile = open('TIME.REL','r')
    for line in infile:
        if len(line.strip()) >0:
            line = line.split()
            line[:] = [int(x) - 1 for x in line] 
            result[line[0]] = line[1:]
    return result
                    
def read_delim(filePath,delim=r"*"):
    result= []
    sep=''
    infile = open(filePath,'r')
    for line in infile:
        if  line.startswith(delim) and len(sep) > 0: 
            result.append(sep)
            sep=''
            continue
        elif len(line.strip()) != 0 and not line.startswith(delim):
            sep= sep+line
    return result
    
def word_check(dict,word):
    return dict.has_key(word)
                
def update_dict(dict,key,value):
    if word_check(dict,key): dict[key] = dict[key] + value
    else: dict[key] = value
         
def tabulate(lst):
    for l in lst:
        sys.stdout.write('\n')
        for t in l:
            sys.stdout.write(str(t)+' '*(20-len(str(t))))

def precision_vs_recall(lst):
    precision = []
    recall = []
    for word in lst[1:]:
        precision.append(word[1])
        recall.append(word[2])
    plt.xlabel('Precision')
    plt.ylabel('Recall')
    plt.plot(precision,recall,'xr-')
    plt.show()
        
def compute_doc_length(docs):
    return {term: len(word) for term, word in enumerate(docs)}
    
def create_tfidf_index(docs, term_occ):
    new = deepcopy(term_occ)
    for key in new.keys():
        res = new[key]
        idf = find_idf(float(docs),len(res)) 
        for key in res.keys():
            ##tf-idf = term frequency* idf
            res[key] = (1 + math.log(res[key],10)) * idf
    return new
    
def term_occurence(docs):
    #Counts the number of times a particular term occurs in all the documents.
    res = defaultdict(lambda: -1)
    count = 0
    for each in docs:
        for word in each:
            if not word_check(res,word):
                new = defaultdict(lambda: -1)                   
                res[word] = new
            if word_check(res[word],count): res[word][count] = res[word][count] + 1
            else: res[word][count] = 1
        count = count + 1
    return res

def find_idf(total_docs,doc_freqs):
    return math.log((float(total_docs)/doc_freqs),10) 

def cosine_search(tfidf,total_docs,query):
    #calculate cosine value given a query return dictionary of related documents with its cosine value
    cos = defaultdict(lambda: -1)
    doc_len = normalize(tfidf) #normalize doc lengths
    query_idf = idf_for_query(tfidf,total_docs,query)
    for key in query_idf.keys():
        for value in tfidf[key].keys():
            res = ((tfidf[key][value] * query_idf[key]) / doc_len[value])
            if word_check(cos,value): cos[value] = cos[value] + res
            else: cos[value] = res
    return cos
             
def idf_for_query(tfidf,total_docs,query):
    query_idf = defaultdict(lambda: -1)
    for word in query:
        if word_check(tfidf,word):       
            word_idf = find_idf(float(total_docs),len(tfidf[word]))
            if word_check(query_idf,word): query_idf[word] = query_idf[word] + word_idf
            else: query_idf[word] = word_idf
    return query_idf
         
def normalize(tfidf):
    #square tf-idf and take the square-root of related documents with term
    doc_len = defaultdict(lambda: -1)
    for key in tfidf.keys():
        for value in tfidf[key].keys():
            res = tfidf[key][value] * tfidf[key][value] 
            if word_check(doc_len,value): doc_len[value] = doc_len[value] + res
            else: doc_len[value] = res
    for key in doc_len.keys(): 
        doc_len[key] = math.sqrt(doc_len[key]) 
    return doc_len

def rsv(tf,total_docs,query_vector):
    rsv = defaultdict(lambda: -1)
    res = defaultdict(lambda: -1)
    for each in query_vector:
        if word_check(tf,each):
            res_2 = find_idf(float(total_docs),len(tf[each]))
            update_dict(res,each,res_2)
    new_idf = res
    for word in new_idf.keys():
        for each in tf[word].keys():
            value = tf[word][each] * new_idf[word] ##tf*IDF #TF not normalized
            update_dict(rsv,each,value)
    return rsv

def BM25(tf,doc_len,query,B,K):
    total_docs = len(doc_len)
    res = defaultdict(lambda: -1)
    for each in query:
        if word_check(tf,each):
            res_2 = find_idf(float(total_docs),len(tf[each]))
            update_dict(res,each,res_2)
    new_idf = res
    mean_result = sum(doc_len.values())/float(len(doc_len))
    res_BM25 = defaultdict(lambda: -1)
    for word in new_idf.keys():
        for each in tf[word].keys():
            value = score(K,B,tf[word][each],doc_len[each],mean_result) * new_idf[word]##tf*IDF #TF not normalized
            update_dict(res_BM25,each,value)
    return  res_BM25


def score(k, b, tf, length, m_length):
    return (k + 1) * tf / (k * ((1 - b) + b * length / m_length) + tf)
    
def Precision(exp,actual):
    result = 0.0 
    for doc in exp:
        if doc in actual:
            result = result + 1.0
    return result/len(exp)
    
def MAP(exp,actual):
    result = 0.0
    for i in range (1,len(exp)):
        if  exp[i-1] in actual:
            result = result + Precision(exp[:i], actual)
    return (result/len(exp))


def gather_all_values(dict,actual,n=20):
    sort_dict = sorted(dict.iteritems(),key=operator.itemgetter(1), reverse=True)
    result = [int(i[0]) for i in sort_dict]
    exp = result[:n]
    Map = MAP(exp,actual)
    exp = set(exp)
    actual=set(actual)
    p = nltk.metrics.precision(actual,exp)
    r = nltk.metrics.recall(actual,exp)
    f1 = nltk.metrics.f_measure(exp,actual)
    return (p,r,f1,Map)

def output(query,rel):
    total_queries = len(query)
    p = 0.0
    r = 0.0
    f1= 0.0
    map= 0.0
    id = 0
    for q in query:
        result = gather_all_values(q,rel[id])
        id = id + 1
        p =p+ result[0]
        r =r+ result[1]
        f1 =f1+ result[2]
        map =map+ result[3]
    p = p / total_queries
    r = r / total_queries
    f1 = f1/total_queries
    map = map/total_queries
    return (p,r,f1,map)
    
def main():
    """ Main method. You should not modify this. """
    documents = read_timeall()
    documents = [stem(tokenize(d)) for d in documents]
    doc_len = compute_doc_length(documents)
    tf = term_occurence(documents)
    tfidf = create_tfidf_index(len(documents), tf)
    queries = read_timeque()
    queries = [stem(tokenize(query)) for query in queries]
    rel = read_timerel()

    cosine = []
    Rsv = []
    BM25_1 = []  
    BM25_2 = [] 
    BM25_3 = [] 
    BM25_4 = [] 
    result = []
    
    for query in queries:
        cosine.append(cosine_search(tfidf,len(documents),query))
        Rsv.append(rsv(tf,len(documents),query))
        BM25_1.append(BM25(tf,doc_len,query,1.0,0.5))
        BM25_2.append(BM25(tf,doc_len,query,1.0,1.0))
        BM25_3.append(BM25(tf,doc_len,query,2.0,0.5))
        BM25_4.append(BM25(tf,doc_len,query,2.0,1.0))

    result.append(('System','Precision','Recall','F1','MAP')) 
    result.append( ('cosine  ',) +output(cosine,rel)) 
    result.append( ('RSV  ',) +output(Rsv,rel))
    result.append(('BM25(1, .5) ',)+output(BM25_1,rel))
    result.append(('BM25(1, 1) ',)+output(BM25_2,rel))
    result.append(('BM25(2, .5) ',)+output(BM25_3,rel)) 
    result.append(('BM25(2, 1) ',)+output(BM25_4,rel))
    precision_vs_recall(result)
    for key in result:
        sys.stdout.write('\n')
        for value in key:
            sys.stdout.write(str(value)+' '*(20-len(str(value))))
    precision_vs_recall(result)

if __name__ == '__main__':
    main()



