""" Assignment 2
You will modify Assignment 1 to support cosine similarity queries.
The documents are read from documents.txt.
The index will store tf-idf values using the formulae from class.
The search method will sort documents by the cosine similarity between the
query and the document (normalized only by the document length, not the query
length, as in the examples in class).
The search method also supports a use_champion parameter, which will use a
champion list (with threshold 10) to perform the search.
"""
from collections import defaultdict
from collections import Counter
import codecs
import math
import re


class Index(object):

    def __init__(self, filename=None, champion_threshold=10):
        """ DO NOT MODIFY.
        Create a new index by parsing the given file containing documents,
        one per line. You should not modify this. """
        if filename:  # filename may be None for testing purposes.
            self.documents = self.read_lines(filename)
            stemmed_docs = [self.stem(self.tokenize(d)) for d in self.documents]
            self.New_words = self.Do_spell_check(stemmed_docs)
            self.doc_freqs = self.count_doc_frequencies(stemmed_docs)
            self.index = self.create_tfidf_index(stemmed_docs, self.doc_freqs)
            self.doc_lengths = self.compute_doc_lengths(self.index)
            self.champion_index = self.create_champion_index(self.index, champion_threshold)

    def Do_spell_check(self,docs):
        new = defaultdict(self.def_dict)
        for word in docs:
            for spell in word:
                if self.word_check(new,spell):
                    new[spell]= new[spell] + 1
                else:
                    new[spell] = 1
        return new
                
    
                
    def edits(self,word):
       alphabet = 'abcdefghijklmnopqrstuvwxyz'
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       deletes    = [a + b[1:] for a, b in splits if b]
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
       inserts    = [a + c + b     for a, b in splits for c in alphabet]
       return set(deletes + transposes + replaces + inserts)
    
    def known(self,words):
        return set(x for x in words if x in self.New_words)
    
    def correct(self,word):
        FINAL = set(res2 for res1 in self.edits(word) for res2 in self.edits(res1) if res2 in self.New_words)
        candidates = self.known([word]) or self.known(self.edits(word)) or FINAL[word] or [word]
        return max(candidates, key=self.New_words.get)

    def word_check(self,dict,word):
        return dict.has_key(word)
                
    def def_dict(self):
        return -1
    

    def compute_doc_lengths(self, index):
        """
        Return a dict mapping doc_id to length, computed as sqrt(sum(w_i**2)),
        where w_i is the tf-idf weight for each term in the document.
        E.g., in the sample index below, document 0 has two terms 'a' (with
        tf-idf weight 3) and 'b' (with tf-idf weight 4). It's length is
        therefore 5 = sqrt(9 + 16).
        >>> lengths = Index().compute_doc_lengths({'a': [[0, 3]], 'b': [[0, 4]]})
        >>> lengths[0]
        5.0
        """
        result = defaultdict(lambda: 0)
        for val in index:
            for doc in index[val]:
                result[doc[0]] += math.pow(doc[1],2)
        for key, value in result.items():
            result[key] = math.sqrt(result[key])
        return result
        """res = {}
        for i in range(len(index[index.keys()[0]])):
            sum = 0
            for val in index.values():
                sum += (val[i][-1])**2
                res[i]=math.sqrt(sum)
        return res"""
        pass

    def create_champion_index(self, index, threshold=10):
        """
        Create an index mapping each term to its champion list, defined as the
        documents with the K highest tf-idf values for that term (the
        threshold parameter determines K).
        In the example below, the champion list for term 'a' contains
        documents 1 and 2; the champion list for term 'b' contains documents 0
        and 1.
        >>> champs = Index().create_champion_index({'a': [[0, 10], [1, 20], [2,15]], 'b': [[0, 20], [1, 15], [2, 10]]}, 2)
        >>> champs['a']
        [[1, 20], [2, 15]]
        >>> champs['b']
        [[0, 20], [1, 15]]
        """
        tempdict = {}
        for k, v in index.items():
            tempdict[k] = sorted(v, key=lambda x:x[1],reverse=True)[:threshold]
        return tempdict 
        pass
    
    def find_tf(self,doc):
        tf = dict(Counter(doc))
        for key in tf.keys():
            tf[key] = 1 + math.log(tf[key],10)
        
        return tf
    def find_idf(self,total_docs,doc_freqs):
        idf = defaultdict(self.def_dict)
        for key in doc_freqs.keys():
            idf[key] = math.log((total_docs/doc_freqs[key]),10) 
        
        return idf

    def create_tfidf_index(self, docs, doc_freqs):
        """
        Create an index in which each postings list contains a list of
        [doc_id, tf-idf weight] pairs. For example:
        {'a': [[0, .5], [10, 0.2]],
         'b': [[5, .1]]}
        This entry means that the term 'a' appears in document 0 (with tf-idf
        weight .5) and in document 10 (with tf-idf weight 0.2). The term 'b'
        appears in document 5 (with tf-idf weight .1).
        Parameters:
        docs........list of lists, where each sublist contains the tokens for one document.
        doc_freqs...dict from term to document frequency (see count_doc_frequencies).
        Use math.log10 (log base 10).
        >>> index = Index().create_tfidf_index([['a', 'b', 'a'], ['a']], {'a': 2., 'b': 1., 'c': 1.})
        >>> sorted(index.keys())
        ['a', 'b']
        >>> index['a']
        [[0, 0.0], [1, 0.0]]
        >>> index['b']  # doctest:+ELLIPSIS
        [[0, 0.301...]]
        """
        """ Another method using only idf computation """
        #res = {}
        #t = sum(isinstance(i, list) for i in docs)
        #for key,val in doc_freqs.items():
        #    res[key] = math.log10(t/val)
        #pos = defaultdict(lambda:[])
        #for docID, lists in enumerate(docs):
        #    for element in set(lists):
        #        pos[element].append([docID, res[element]])
        #return pos
        
        final = defaultdict(self.def_dict)
        total_docs = float(len(docs)) 
        new_tf = defaultdict(self.def_dict)
        for key in doc_freqs.keys():
            new_tf[key] = math.log((total_docs/doc_freqs[key]),10)
        for i in range(0,len(docs)):
            new_idf = dict(Counter(docs[i]))
            for key in new_idf.keys():
                new_idf[key] = 1 + math.log(new_idf[key],10)
            for key in new_idf.keys():
                result = [i,new_tf[key]*new_idf[key]]
                if self.word_check(final, key):
                    res = final[key]
                    res.append(result)
                    final[key] = res
                else:
                    final[key] = [result]
        return final

        pass

    
    def count_doc_frequencies(self, docs):
        """ Return a dict mapping terms to document frequency.
        >>> res = Index().count_doc_frequencies([['a', 'b', 'a'], ['a', 'b', 'c'], ['a']])
        >>> res['a']
        3
        >>> res['b']
        2
        >>> res['c']
        1
        """
        
        tmp = []
        lst = {}
        for item in docs: tmp += set(item)
        for key in tmp: lst[key] = lst.get(key, 0) + 1
        return lst
        pass
    
    def query_to_vector(self, query_terms):
        """ Convert a list of query terms into a dict mapping term to inverse document frequency.
	using log(N / df(term)), where N is number of documents and df(term) is the number of documents
        that term appears in.
        Parameters:
        query_terms....list of terms
        """
        
        query_doc_freq = defaultdict(self.def_dict)
        for word in query_terms:
            query_doc_freq[word]=self.doc_freqs[word]
        
        result = defaultdict(self.def_dict)
        for key in query_doc_freq.keys():
            result[key] = math.log((float(len(self.documents))/query_doc_freq[key]),10) 
        return result
    
        pass
        

    def search_by_cosine(self, query_vector, index, doc_lengths):
        """
        Return a sorted list of doc_id, score pairs, where the score is the
        cosine similarity between the query_vector and the document. The
        document length should be used in the denominator, but not the query
        length (as discussed in class). You can use the built-in sorted method
        (rather than a priority queue) to sort the results.
        The parameters are:
        query_vector.....dict from term to weight from the query
        index............dict from term to list of doc_id, weight pairs
        doc_lengths......dict from doc_id to length (output of compute_doc_lengths)
        In the example below, the query is the term 'a' with weight
        1. Document 1 has cosine similarity of 2, while document 0 has
        similarity of 1.
        >>> Index().search_by_cosine({'a': 1}, {'a': [[0, 1], [1, 2]]}, {0: 1, 1: 1})
        [(1, 2), (0, 1)]
        """
                
        scores = defaultdict(lambda: 0)
        for query_term, query_weight in query_vector.items():
            for doc_id, doc_weight in index[query_term]:
                scores[doc_id] += query_weight * doc_weight  
        for doc_id in scores:
            scores[doc_id] /= doc_lengths[doc_id]
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
        pass

    def search(self, query, use_champions=False):
        """ Return the document ids for documents matching the query. Assume that
        query is a single string, possible containing multiple words. Assume
        queries with multiple words are phrase queries. The steps are to:
        1. Tokenize the query (calling self.tokenize)
        2. Stem the query tokens (calling self.stem)
        3. Convert the query into an idf vector (calling self.query_to_vector)
        4. Compute cosine similarity between query vector and each document (calling search_by_cosine).
        Parameters:
        query...........raw query string, possibly containing multiple terms (though boolean operators do not need to be supported)
        use_champions...If True, Step 4 above will use only the champion index to perform the search.
        """
        
        stemmed_query = self.stem(self.tokenize(query))
        for i in range(0,len(stemmed_query)):
            stemmed_query[i] = self.correct(stemmed_query[i])
        query_vec = self.query_to_vector(stemmed_query)
        result_docIds = []
        if use_champions==True:
            result_docIds = self.search_by_cosine(query_vec, self.champion_index, self.doc_lengths)
        else:
            result_docIds = self.search_by_cosine(query_vec, self.index, self.doc_lengths)
        return result_docIds
        pass

    def read_lines(self, filename):
        """ DO NOT MODIFY.
        Read a file to a list of strings. You should not need to modify
        this. """
        return [l.strip() for l in codecs.open(filename, 'r+b', 'utf-8').readlines()]

    def tokenize(self, document):
        """ DO NOT MODIFY.
        Convert a string representing one document into a list of
        words. Retain hyphens and apostrophes inside words. Remove all other
        punctuation and convert to lowercase.
        >>> Index().tokenize("Hi there. What's going on? first-class")
        ['hi', 'there', "what's", 'going', 'on', 'first-class']
        """
        return [t.lower() for t in re.findall(r"\w+(?:[-']\w+)*", document)]

    def stem(self, tokens):
        """ DO NOT MODIFY.
        Given a list of tokens, collapse 'did' and 'does' into the term 'do'.
        >>> Index().stem(['did', 'does', 'do', "doesn't", 'splendid'])
        ['do', 'do', 'do', "doesn't", 'splendid']
        """
        return [re.sub('^(did|does)$', 'do', t) for t in tokens]


def main():
    """ DO NOT MODIFY.
    Main method. Constructs an Index object and runs a sample query. """
    indexer = Index('documents.txt')
    for query in ['pop love song', 'chinese american', 'city']:
        print '\n\nQUERY=', query
        print '\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query)[:10]])
        print '\n\nQUERY=', query, 'Using Champion List'
        print '\n'.join(['%d\t%e' % (doc_id, score) for doc_id, score in indexer.search(query, True)[:10]])

if __name__ == '__main__':
    main()
