""" Assignment 0

You will implement a simple in-memory boolean search engine over the jokes
from http://web.hawkesnest.net/~jthens/laffytaffy/.

The documents are read from documents.txt.
The queries to be processed are read from queries.txt.

Your search engine will only need to support AND queries. A multi-word query
is assumed to be an AND of the words. E.g., the query "why because" should be
processed as "why AND because."
"""

# Some imports you may want to use.
from collections import defaultdict
import re


def read_lines(filename):
    """ Read a file to a list of strings. You should not need to modify
    this. """
    return [l.strip() for l in open(filename, 'rt').readlines()]


def tokenize(document):
    """ Convert a string representing one document into a list of
    words. Remove all punctuation and split on whitespace.
    >>> tokenize("Hi there. What's going on?")
    ['hi', 'there', 'what', 's', 'going', 'on']
    """
    #hey = document.lower() 
    #b = hey.split('   ')
    #c = [ re.findall(r'\w+',x) for x in b ]
    #return c
    hey = document.lower() 
    return re.findall(r'\w+', hey)
    pass


def create_index(tokens):
    """
    Create an inverted index given a list of document tokens. The index maps
    each unique word to a list of document ids, sorted in increasing order.
    >>> index = create_index([['a', 'b'], ['a', 'c']])
    >>> sorted(index.keys())
    ['a', 'b', 'c']
    >>> index['a']
    [0, 1]
    >>> index['b']
    [0]
    >>> index['c']
    [1]
    """
    index = defaultdict(list)
    for i, word in enumerate(tokens):
        for text in word:
            index[text].append(i)
    return index                             #sorted(index.keys())
    pass


def intersect(list1, list2):
    """ Return the intersection of two posting lists. Use the optimize
    algorithm of Figure 1.6 of the MRS text.
    >>> intersect([1, 3, 5], [3, 4, 5, 10])
    [3, 5]
    >>> intersect([1, 2], [3, 4])
    []
    """
    #result = []                     
    #for l in list1:               
     #   if l in list2:            
      #      result.append(l)        
    #return result
    res = []
    docId = 0
    docId2 = 0
    while docId<len(list1) and docId2<len(list2):
        if list1[docId] == list2[docId2]:
            res.append(list1[docId])
            docId = docId+1
            docId2 = docId2+1
        elif list1[docId] < list2[docId2]:
            docId = docId+1
        else:
            docId2 = docId2+1
            
    return res
    
    pass

def sort_by_num_postings(words, index):
    """
    Sort the words in increasing order of the length of their postings list in
    index.
    >>> sort_by_num_postings(['a', 'b', 'c'], {'a': [0, 1], 'b': [1, 2, 3], 'c': [4]})
    ['c', 'a', 'b']
    """
    return sorted(words,key=lambda x : len(index[x]))
    pass


def search(index, query):
    """ Return the document ids for documents matching the query. Assume that query is a single string, possible containing multiple words. The steps are to:
    1. tokenize the query
    2. Sort the query words by the length of their postings list
    3. Intersect the postings list of each word in the query.
    E.g., below we search for documents containing 'a' and 'b':
    >>> search({'a': [0, 1], 'b': [1, 2, 3], 'c': [4]}, 'a b')
    [1]
    """
    data = tokenize(query)
    sorting = sort_by_num_postings(data,index)
    i = 1
    inter = []
    if(len(sorting) > 0):
        inter = index[sorting[0]]
    while i < len(sorting):
        inter = intersect(inter,index[sorting[i]])
        i += 1
    return inter
    pass


def main():
    """ Main method. You should not modify this. """
    documents = read_lines('documents.txt')
    tokens = [tokenize(d) for d in documents]
    index = create_index(tokens)
    queries = read_lines('queries.txt')
    for query in queries:
        results = search(index, query)
        print '\n\nQUERY:', query, '\nRESULTS:\n', '\n'.join(documents[r] for r in results)


if __name__ == '__main__':
    main()
