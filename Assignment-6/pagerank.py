""" Assignment 6: PageRank. """
from collections import defaultdict
import glob
from bs4 import BeautifulSoup


def parse(folder, inlinks, outlinks):
    """
    Read all .html files in the specified folder. Populate the two
    dictionaries inlinks and outlinks. inlinks maps a url to its set of
    backlinks. outlinks maps a url to its set of forward links.
    """
    path = '.\\'+folder+'\\*.html'
    for file in glob.glob(path):
        infile = open(file,'r') 
        html_doc =  infile.readlines()
        inlink = infile.name.split('\\')[-1] 
        soup = BeautifulSoup(''.join(html_doc))
        #print soup.prettify()
        #for i in soup.body:
        #   print i
        config_links(soup,inlinks,outlinks,inlink)
    pass

def config_links(parse,inlinks,outlinks,inlink):
    for link in parse.findAll('a'): # To find all the 'a' tags 
        outlink = link.get('href')
        outlinks[inlink].add(outlink)
        inlinks[outlink].add(inlink)
        
def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = 1-b + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0
    """
    Rw = {}
    pagerank = {}
    for i in urls:
        pagerank[i] = 1.0 #Initialize all scores to 1.0
    for i in range(0,iters):
        for url in pagerank:
            Rw[url] = pagerank[url]/len(outlinks[url])
        for url in urls:
            result_sum = 0.0
            for link in inlinks[url]: #sum_{w in B_u} R(w) / (|F_w|)
                result_sum = result_sum + Rw[link]
            pagerank[url] = 1.0-b+b*result_sum
    return pagerank
    pass

def run(folder, b):
    """ Do not modify this function. """
    inlinks = defaultdict(lambda: set())
    outlinks = defaultdict(lambda: set())
    parse(folder, inlinks, outlinks)
    urls = sorted(set(inlinks) | set(outlinks)) 
    ranks = compute_pagerank(urls, inlinks, outlinks, b=b)
    print 'Result for', folder, '\n', '\n'.join('%s\t%.3f' % (url, ranks[url]) for url in sorted(ranks))


def main():
    """ Do not modify this function. """
    run('set1', b=.5)
    run('set2', b=.85)


if __name__ == '__main__':
    main()
