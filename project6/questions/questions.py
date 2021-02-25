import nltk
import sys

import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    # Iterate over files in directory
    for doc in os.listdir(directory):

        # Get path of file
        path = os.path.join(directory, doc)

        # Open file
        with open(path) as reader:

            # Get filename
            name = os.path.basename(os.path.normpath(path)).rstrip(".txt")
            
            # Get contents
            files[name] = reader.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Add a word if it's not in stopwords and it's not a punctuation
    words = [
        word.lower() for word in nltk.word_tokenize(document)
        if word.lower() not in (nltk.corpus.stopwords.words("english") +
                                list(string.punctuation))
    ]
    
    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.

    idf = ln(Number of documents /
             Number of documents in which the word appears)
    """

    # Number of documents
    docNum = len(documents)

    idfs = dict()
    for document in documents:
        for word in documents[document]:
            # Skip words that are already in a dict
            if word in idfs:
                continue
            
            # Calculate number of documents in which the word appears
            wordDocNum = 0
            for document in documents:
                if word in documents[document]:
                    wordDocNum += 1
            
            # Calculate idfs
            idfs[word] = math.log(docNum / wordDocNum, math.e)
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    topFiles = dict()
    for document in files:

        # Initialize document's tf-idf value
        topFiles[document] = 0
        for word in query:
            if word in idfs:

                # Calculate tf
                tf = files[document].count(word)
                
                # Calculate tf-idf
                tfidf = tf * idfs[word]

                # Assign tf-idf value to document
                topFiles[document] += tfidf

    # Sort and return top `n` files
    return sorted(topFiles, key=topFiles.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    topSent = dict()
    for sentence in sentences:

        # Initialize sentence's `idf` and query term density values
        topSent[sentence] = [0, 0]

        # Calculate query term density (`length of intersection` / 
        #                               `length of sentence`)
        qtd = (len(query.intersection(sentences[sentence])) /
               len(set(sentences[sentence])))

        # Assign `qtd` to sentence
        topSent[sentence] = [0, qtd]

        # Add word's `idf` values to sentence if word in sentence and in `idf`
        for word in query:
            if word in sentences[sentence] and word in idfs:
                topSent[sentence][0] += idfs[word]

    # Sort sentences by `idf`, then by `qtd`
    topSent = sorted(topSent,
                     key=lambda key: (topSent[key][0], topSent[key][1]),
                     reverse=True)

    # Return top `n` sentences
    return topSent[:n]


if __name__ == "__main__":
    main()
