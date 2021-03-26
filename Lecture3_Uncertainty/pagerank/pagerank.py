import os
import random
import re
import sys
from numpy.random import choice

DAMPING = 0.85
SAMPLES = 100000
epsilon = 0.001

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
   # initialize dictionay with keys from corpus
    transition = {}
    for i in list(corpus.keys()):
       transition[i] = 0

   # For all the pages the current page has link to, random select one and assign damping_factor to it
    if len(corpus[page]) > 0:
        for p in corpus[page]:
            transition[p] = damping_factor/len(corpus[page])
    else: # giving equal probability to all pages in the corpus
        for p in transition:
            transition[p] = 1/len(list(corpus.keys()))
        return transition
    
   # For pages not linked to the given page, randomly pick one and assign 1-damping_factor
   # transition[random.sample([i for i in list(corpus.keys()) 
   #                           if i not in corpus[page]],1)[0]] = round(1 - damping_factor,5)
   
   # random choose a page 
    for p in transition:
      transition[p] += round(1 - damping_factor,5)/len(list(corpus.keys()))
    
    
    return transition
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Initialize count
    count = 1
    
    # get list of pages
    pagelist = list(corpus.keys())
    
    # Initialize results
    res = {}
    for i in pagelist:
       res[i] = 0
    
    # choose the first page
    page = random.sample(pagelist,1)[0]
    
    # sampling   
    while count <= n:
        # get transition model 
        transitionModel = transition_model(corpus, page, damping_factor)
        
        # random next page
        nextPage = choice(list(transitionModel.keys()),
                          1,
                          p = list(transitionModel.values()))[0]
        
        # update count
        res[nextPage] += 1
        
        # update page and count
        page = nextPage
        count += 1
        
    # normalize probabilities
    for x in res:
        res[x] = res[x]/n
    
    return res
    
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
  
            
    
    # Initialize flag for loop
    flag = True
    
    # get list of pages
    pagelist = list(corpus.keys())
    
    # update corpus to add all pages to pages with no links
    for p in corpus:
        if len(corpus[p]) == 0:
            corpus[p] = set(pagelist)
            
    # Initialize results
    res = {}
    for i in pagelist:
       res[i] = 1/len(pagelist)
    
    count = 1
    
    # Using the iterative algorithm
    while flag:
      nextRes = res.copy()
      for p in nextRes:
          nextRes[p] = update_pagerank(corpus,p,damping_factor,nextRes)
          
      # Check for convergence
      for p in nextRes:
          if abs(nextRes[p] - res[p]) >= epsilon:
              break
          flag = False
      
      # Update results
      res = nextRes.copy()
      count += 1
    #print(count)
    return res
    
    
    #raise NotImplementedError

def update_pagerank(corpus,page,damping_factor,pageRank):
    """
    Return the updated PageRank for the given page by applying the iterative 
    formula

    """
    pagelist = list(corpus.keys())
    
    d = damping_factor
    
    n = len(pagelist)
    
    # get incoming pages for the given page
    incomingPage = []
    for p in corpus:
        if page in corpus[p]:
            incomingPage.append(p)
    
    # calcualte the second part of the formula
    summation = 0
    for p in incomingPage:
        numLinks = len(corpus[p])
        pageRank_p = pageRank[p]
        summation += pageRank_p/numLinks
    
    
    updatedPageRank = (1-d)/n + d*summation
    
    return updatedPageRank
     
     


if __name__ == "__main__":
    main()
