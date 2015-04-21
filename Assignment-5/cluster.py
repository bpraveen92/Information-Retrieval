"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter
import io
import math
import numpy as np
from itertools import starmap,izip
from operator import mul
from collections import defaultdict

class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        Each iteration consists of calls to compute_means and compute_clusters.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector)
        See Log.txt for expected output.
        """
        self.mean_vector = documents[0:self.k] 
        self.documents = documents
        for i in range (0,iters):
            self.clusters = self.compute_clusters(documents)
            self.mean_vector = self.compute_means(self.clusters,documents)
        self.clus = sorted(self.clusters, key=lambda ele: ele[2])
        
        pass

    def compute_means(self,clusters,docs):
        """ Compute the mean vectors for each cluster (storing the results in an
        instance variable)."""
        total1 = defaultdict(lambda: Counter())#Total of all clusters
        total2 = defaultdict(lambda: 0)#Number of clusters
        self.error_value = 0.0
        for cluster in clusters:
            d_id,c_id,distance = cluster
            total1[c_id].update(docs[d_id])
            total2[c_id] += 1
        self.e = self.error(clusters)
        return self.display(total1,total2)
        pass
    
    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable). """
        res = []
        cluster = []
        for doc in self.mean_vector:
            dp = doc.values()
            res.append(sum(starmap(mul,izip(dp,dp)))) 
        for doc in range(0,len(documents)):
            cluster.append((doc,)+ self.find_min_dist(documents[doc],res))
        return cluster
        
    def find_min_dist(self,doc,res):
        vector = []
        for i in range(0,len(self.mean_vector)):
            vector.append((i, self.distance(doc, self.mean_vector[i], res[i])))
        comp = vector[0]
        for ele in vector:
            if ele[1] < comp[1]:
                comp = ele
        return comp       
        pass

    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        value = doc.values()
        dot_pro = sum(starmap(mul,izip(value,value)))#improves time efficiency than numpy built in dot function
        res = 0.0
        for key in doc.keys():
            if key in mean:
                res += mean[key]*doc[key]
        result = math.sqrt(mean_norm + dot_pro - 2.0*res)
        return result

    def error(self, documents):
        """ Return the error of the current clustering, defined as the sum of the
        Euclidean distances between each document and its assigned mean vector."""
        error_value = 0.0
        for cluster in documents:
            d_id,c_id,distance = cluster
            error_value = error_value + distance
        return error_value        
        pass
    
    def display(self,total1,total2):
        #calculation of average
        result = [] 
        for ele in sorted(total1.keys()): 
            doc =  float(total2[ele])
            for key in total1[ele].keys():
                total1[ele][key] = total1[ele][key]/doc
            result.append(total1[ele])
        disp = [ele[1]  for ele in sorted(total2.items())]
       
        print disp
        print  self.e
        return result

    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster, sorted by distance to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (which will be out of order from the original
        document).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
       
        top = defaultdict(lambda: [])
        for cluster in self.clus:
            d,c,dist = cluster
            top[c] = top[c] + [(dist,d)]
        return self.Final_print(top)
        
    def Final_print(self,dicto,n=10):
        #Printing according to cluster number
        for clus_num in sorted(dicto.keys()):
            count = 0
            print 'CLUSTER  '+str(clus_num)
            for doc in sorted(dicto[clus_num]):
                if count == n:
                    break
                elif len(self.documents[doc[1]]) > 3:
                    print ' '.join([unicode(ele).encode('utf8') for ele in self.documents[doc[1]]])
                    count += 1
        pass


def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    counters = [Counter(d.keys()) for d in docs]
    total = sum(counters, Counter()) 
    keys = set(k for k, v in total.items() if v >= min_df)#Create set with keys of high frequency
    results = (Counter({k: v for k, v in d.items() if k in keys}) for d in docs)#Reconstruct counters using high frequency keys
    return filter(None, results)#With filter(None, ...) I take only the non empty counters.
    
    pass


def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with io.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles

def main():
    """ DO NOT MODIFY. """
    profiles = read_profiles('profiles.txt')
    print 'read', len(profiles), 'profiles.'
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
