Edit this file in your private repository to provide answers to the following questions.

1. Consider merging the following two lists, where the first list has skip pointers.
![skips](skips.png)
  1. How often is a skip pointer followed (i.e., p1 is advanced to skip(p1))?

    **The skip pointer is followed only once, 24->75.**

  2. How many postings comparisons will be made by this algorithm while intersecting the two lists?

    **18 postings comparisons will be made by the algorithm in total,
(3,3),(5,5),(9,89),(15,89),(24,89),(75,89),(92,89),(81,89),(84,89),(89,89),(95,92),(95,115),(95,96),(97,96),(97,97),(99,100),(100,100),(101,115)** 
  
  3. How many postings comparisons would be made if the postings lists are intersected without the use of skip pointers?

    **19 postings comparisons would be made if the postings lists are intersected without the use of skip pointers.
(3,3),(5,5),(89>9),(89,15),(89,24),(89,39),(89,60),(89,68),(89,75), (89,81),(89,84),(89,89),(95,92),(95,96),(97,96),(97,97),(99,100),(100,100),(101,115)**


2. Compute the Levenshtein edit distance between *paris* and *alice*. Fill in the 5 × 5 table below of
distances between all preﬁxes as computed by the algorithm in Figure 3.5 in [MRS](http://nlp.stanford.edu/IR-book/pdf/03dict.pdf). Cell (*i*, *j*) should store the minimum edit distance between the first *i* characters of *alice* and the first *j* characters of *paris* (as in the bottom right number of each cell in Figure 3.6).

  |       |   | p | a | r | i | s |
  |-------|---|---|---|---|---|---|
  |       | 0 | 1 | 2 | 3 | 4 | 5 |
  | **a** | 1 | 1 | 1 | 2 | 3 | 4 |
  | **l** | 2 | 2 | 2 | 2 | 3 | 4 |
  | **i** | 3 | 3 | 3 | 3 | 2 | 3 |
  | **c** | 4 | 4 | 4 | 4 | 3 | 3 |
  | **e** | 5 | 5 | 5 | 5 | 4 | 4 |

3. (Inspired by [H Schütze](http://www.cis.uni-muenchen.de/~hs/teach/13s/ir/).)We define a *hapax legomenon* as a term that occurs exactly once in a collection. We want to estimate the number of hapax legomena using Heaps’ law and Zipf’s law.
    1. How many unique terms does a web collection of 400,000,000 web pages containing 400 tokens on average have? Use the Heaps parameters k = 100 and b = 0.5.
	**Heaps Law: M = K.Tb with M being the size of the vocabulary and T the number of tokens in the collection.
	
       M = 100*(400,000,000 * 400)0.5 
	 = 40,000,000  
    2. Use Zipf’s law to estimate the proportion of the term vocabulary of the collection that consists of hapax legomena. You may want to use the approximation 1/1 + 1/2 + ... + 1/*n* = ln *n*
	**
Zipf’s law: cfi ∝ 1/i ⇒ ∃c : cfi = c * 1/i

Calculate c:

The sum of all collection frequencies is the total number of tokens T:
(400, 000, 000 * 400) = T = ∑Mi=1 c * 1/I 

≈ c * ln(40, 000, 000) ≈ 17.504 * c

⇒ c = T/17.504 ≈ 2 * 10^10

Zipf’s law: cfi ∝ 1/i ⇒ cfi = 2 · 10^10 * 1/i

Calculate the frequency of the least frequent term (i.e. term with rank
i = 40, 000, 000):

cf40, 000, 000 = 2 * 10^10 / 40,000,000 
	    
    = 1/2 * 1000

⇒ The least frequent term appears more than once! 
⇒ Based on Heap’s law and Zipf’s law, there are no hapax legomena in the collection!
⇒ The proportion of hapax legomena is 0. **
    
   3. Do you think that the estimate you get is correct? Why or why not?

  **This prediction is not correct. Generally, roughly 50% of the vocabulary consists of hapax legomena (but this depends on the collection!)**

