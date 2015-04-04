Edit this file in your private repository to provide answers to the following questions (from MRS).

1. Extend the postings merge algorithm to arbitrary Boolean query formulas. What is
its time complexity? For instance, consider:

  `(Brutus OR Caesar) AND NOT (Antony OR Cleopatra)`

  Can we always merge in linear time? Linear in what? Can we do better than this?

  ** Yes we can always merge in linear time. We can do better by trying to get frequency occurrence for all terms, estimate the size of each OR by the sum of its frequencies. 
    Process in increasing order of OR sizes. The time complexity is O(m+n) where m equals O(a+b) that is the time taken to perform the OR operation between Brutus & Caesar,
and n equals O(c+d) which is the time taken to perform the OR operation between Antony and Cleopatra.
Process in linear  time a CNF formula: 
	(C11OR C12... OR C1k1) AND …..AND 
	(Cn1OR Cn2… OR Cnkn)
Algorithm: 
If Cij= NOT Term then use the  Doc id intervals not containing Term while traversing the posting list of Term
For each (Ci1OR Ci2... OR Ciki) implicitely  consider the posting interval list Ii union of the intervals for every Term Cij while traversing the posting lists
Find Doc ids contained in all intervals I1,….,In  **

2. If the query is:

  `friends AND romans AND (NOT countrymen)`

  How could we use the frequency of countrymen in evaluating the best query evaluation order? In particular, propose a way of handling negation in determining the order of query processing.
  
  **
For each of the n terms, get its postings, Process in the order of increasing frequency, start with smallest set and then keep cutting further.If countrymen is more frequent then it can be 
used to remove documents by where it does not exist.
Count for word X in (documents where word X occurs)
For Word X the count for !X in 
((number of total documents)-(documents where word X occurs)).**
  
3. For a conjunctive query, is processing postings lists in order of size guaranteed to be
optimal? Explain why it is, or give an example where it isn’t.

  ** Processing postings list in order of size (i.e. the shortest postings list first) is usually a good approach.
But it is not optimal e. g. in a conjunctive query with three terms:
	word 1 = 1,25,33
	word 2 = 2,13,44,75
	word 3 = 10,31,20,60,48.
As we can see there is no document containing all three query terms. If we would have checked the
first posting of the third list right at the beginning, we would have noticed that there is no intersection
between the first and the third postings list. That would make any further search superfluous. **
