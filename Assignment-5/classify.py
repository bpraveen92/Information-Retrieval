"""
Assignment 4. Implement a Naive Bayes classifier for spam filtering.
You'll only have to implement 3 methods below:
train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.
"""
from __future__ import division
import glob
import math
import collections
from collections import defaultdict




class Document(object):
    """ A Document. DO NOT MODIFY.
    The instance variables are:
    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename):
        self.filename = filename
        self.label = 'spam' if 'spmsg' in filename else 'ham'
        self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):
   

    def train(self, documents):
        """
        TODO: COMPLETE THIS METHOD.
        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your book.
        """
        
        vocab = []
        count_docs = len(documents)
        unique_vocab = []
        self.label_count = defaultdict(int)
        self.prior = defaultdict(float)
        concat_spam = []
        concat_ham = []
        
        for fname in documents:
            self.label_count[fname.label] += 1
            if fname.label == "spam":
                for doc in fname.tokens:
                    concat_spam.append(doc)
            elif fname.label == "ham":
                for doc in fname.tokens:
                    concat_ham.append(doc)
            for doc in fname.tokens:
                vocab.append(doc)
        unique_vocab = list(set(vocab))
        
        for label in self.label_count:
            self.prior[label] = float(self.label_count[label]) / count_docs
  
        self.cond_prob_spam = defaultdict(lambda:0)
        self.cond_prob_ham = defaultdict(lambda:0)
        
        count_tokens_spam = collections.Counter(concat_spam)
        count_tokens_ham = collections.Counter(concat_ham)
        
        for word in unique_vocab:
            self.cond_prob_spam[word] = float (count_tokens_spam[word] + 1) / float ( len(concat_spam) + len(unique_vocab))
            self.cond_prob_ham[word] = float (count_tokens_ham[word] + 1) / float ( len(concat_ham) + len(unique_vocab))
        
        pass

    def classify(self, documents):
        """
        TODO: COMPLETE THIS METHOD.
        Return a list of strings, either 'spam' or 'ham', for each document.
        documents....A list of Document objects to be classified.
        """
         
        final = []
        result = ''
        score = defaultdict(float)
        for fname in documents:
            for key in self.label_count:
                score[key] = math.log(self.prior[key],10)
            for doc in list(set(fname.tokens)):
               if (self.cond_prob_spam[doc] > 0 and self.cond_prob_ham[doc] > 0):
                   score["spam"] += math.log(self.cond_prob_spam[doc],10) * fname.tokens.count(doc)
                   score["ham"] += math.log(self.cond_prob_ham[doc],10) * fname.tokens.count(doc)
            result = max(score, key=score.get) 
            final.append(result)
        return final
        pass

def evaluate(predictions, documents):
    """
    TODO: COMPLETE THIS METHOD.
    Evaluate the accuracy of a set of predictions.
    Print the following:
    accuracy=xxx, yyy false spam, zzz missed spam
    where
    xxx = percent of documents classified correctly
    yyy = number of ham documents incorrectly classified as spam
    zzz = number of spam documents incorrectly classified as ham
    See the provided log file for the expected output.
    predictions....list of document labels predicted by a classifier.
    documents......list of Document objects, with known labels.
    """
    
    false_spam = 0
    false_ham = 0
    correctly_classified = 0
    for i in range(0,len(documents)):
        if documents[i].label == predictions[i] :
            correctly_classified += 1
        else:
            if predictions[i] == 'spam':
                false_spam += 1
            else:
                false_ham += 1
    acc_value = (correctly_classified/float(len(documents)))
    print "accuracy=", acc_value,"," , false_spam, "false spam,", false_ham , "missed spam"
    
def main():
    """ DO NOT MODIFY. """
    train_docs = [Document(f) for f in glob.glob("train/*.txt")]
    print 'read', len(train_docs), 'training documents.'
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(f) for f in glob.glob("test/*.txt")]
    print 'read', len(test_docs), 'testing documents.'
    predictions = nb.classify(test_docs)
    evaluate(predictions, test_docs)

if __name__ == '__main__':
    main()
