import os
import random
import re
import sys

from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


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
    # Initialize output dict
    output = {}
    for page in corpus.keys():
        output[page] = 0

    # Check page links and add probability
    links = corpus[page]
    linkAmount = len(links)
    if linkAmount:
        prob = damping_factor / linkAmount
        for link in links:
            output[link] += prob
    
    # Add random probability
    prob = (1 - damping_factor) / len(corpus)
    for link in output:
        output[link] += prob
    
    return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Choose random page
    page = random.choice(list(corpus.keys()))

    pages = []
    for i in range(n):
        # Get probabilities
        transition = transition_model(corpus, page, damping_factor)

        # Choose page
        page = random.choices(list(transition.keys()), weights=list(transition.values()), k=1)[0]

        # Count page
        pages.append(page)
    
    # Calculate PageRank value
    pages = dict(Counter(pages))
    for page in pages:
        pages[page] = pages[page] / n
    return pages

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize output
    PR = {}
    N = len(corpus)
    for page in corpus:
        PR[page] = 1 / N
    
    # 
    d = damping_factor
    while True:
        
        


if __name__ == "__main__":
    main()
