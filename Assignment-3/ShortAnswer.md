Edit this file and push to your private repository to provide answers to the following questions.

1. In `searcher.py`, why do we keep an inverted index instead of simply a list
of document vectors (e.g., dicts)? What is the difference in time and space
complexity between the two approaches?

    **The inverted index is the main data structure of our search engine. We will use a Hashtable (python’s dictionary) to store the inverted index in memory. 
The reason is we will perform lots of lookups (one for every term in the document), and we will also add lots of keys (every term is a key), so we want these operations to be very efficient. 
Since Hashtables have average O(1) lookup time and amortized O(1) insertion time, they are very suitable for our needs. By using an inverted index its faster to retrieve relevant documents given a corpus of documents.
The inverted index consists of a postings list, which basically keeps hold of the positions of term occurrences within the document.
The reason is to answer the phrase queries we need positional information, because we want to check whether the terms in the query appear in the specified order. 
Without knowing the positions of the terms in the document, we can only check whether the query terms simply appear in a document. To verify the order, we need to know their positions.  
Hence, the time and space complexity to locate a word in a set of documents could be O(log(n))+ O(m), where n is the total number of documents and m is the maximum size of each document.
On the other hand, the document vector is just a dictionary collection of the words occurring in the documents it has no information on which term occurs where exactly in the documents(positions:Unknown)
The complexity of a document vector is supposedly o(m^2).  **

2. Consider the query `chinese` with and without using champion lists.  Why is
the top result without champion lists absent from the list that uses champion
lists? How can you alter the algorithm to fix this?

    **Algorithm:
We compute the scores(say a(b)) of the documents by using static measures (pageranks).
-->Ordering the postings list of documents in the decreasing order of the scores. 
-->Computation of the cosine similarity between these documents and the given query. The netscore will result to be the sum of a(b) + cosine_similarity(m,b)     
-->We now find that the cosine_scores scores are normalized by document length, by adding the a(b) to the cosine score we get the documents that have a better match.**

3. Describe in detail the data structures you would use to implement the
Cluster Pruning approach, as well as how you would use them at query time.

    **step 1 : We perform the clustering of document vectors. Then at query time, we consider only documents in a small number of clusters as candidates for which we compute cosine scores.
Specifically, the preprocessing step is as follows:
Pick sqrt(N) documents at random from the collection. Call these asleaders.
For each document that is not a leader, we compute its nearest leader.
We refer to documents that are not leaders as followers. Intuitively, in the partition of the followers induced by the use of sqrt(N) randomly chosen leaders, the expected number of followers for each leader is  N/sqrt(N) = sqrt(N). 
Next, query processing proceeds as follows:
1.Given a query q, find the leader L that is closest to q. This entails computing cosine similarities from q to each of the sqrt(N) leaders.
2.The candidate set A consists of L together with its followers. We compute the cosine scores for all documents in this candidate set.
The use of randomly chosen leaders for clustering is fast and likely to reflect the distribution of the document vectors in the vector space: a region of the vector space that is dense in documents is likely to produce multiple leaders and thus a finer partition into sub-regions

Variations of cluster pruning introduce additional parameters b1 and b2, both of which are positive integers. In the pre-processing step we attach each follower to its b1 closest leaders, rather than a single closest leader. At query time we consider the b2 leaders closest to the query q. 
Clearly, the basic scheme corresponds to the case b1=b2=1. Further, increasing b1 or b2 increases the likelihood of finding K documents that are more likely to be in the set of true top-scoring K documents, at the expense of more computation**
