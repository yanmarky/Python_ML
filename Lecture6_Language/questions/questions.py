import nltk
import sys
import string
import os
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
    continueFlag = True
    while continueFlag:
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

        if input("Continue(Y/N)?: ")=="N":
            continueFlag = False


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    fList = [item for item in os.listdir(directory) if ".txt" in item]
    res = dict()
    for file in fList:
        with open(os.path.join(directory,file),encoding="utf8") as f:
            s = f.read()
            res[file] = s
    return res


    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document)

    wordList = []
    for word in tokens:
        if word not in string.punctuation:
            if word.lower() not in nltk.corpus.stopwords.words("english"):
                wordList.append(word.lower())
    return wordList
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = []
    for filename in documents:
        words = words + documents[filename]
    wordList = set(words)

    wordIDF = dict()
    nDoc = len(documents)
    for word in wordList:
        nAppear = 0
        for filename in documents:
            if word in documents[filename]:
                nAppear += 1
        wordIDF[word] = math.log(nDoc/nAppear)

    return wordIDF




    #raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    fileScore = list()
    for filename in files:
        tf_IDF = 0
        for words in query:
            tf = files[filename].count(words)/len(files[filename])
            tf_IDF += tf*idfs[words]
        fileScore.append((filename,tf_IDF))
    fileScore.sort(key = lambda x: x[1],reverse=True)
    res = []
    for i in range(min(n,len(files))):
        res.append(fileScore[i][0])

    return res

    #raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentenceScore = []
    for sentence in sentences:
        score = 0
        densityCount = 0
        for word in query:
            if word in sentences[sentence]:
                #print(f'Word:{word},IDF:{idfs[word]}')
                score += idfs[word]
                densityCount += sentences[sentence].count(word)
        sentenceScore.append((sentence,score,densityCount/len(sentences[sentence])))
    sentenceScore.sort(reverse=True,key = lambda x: (x[1],x[2]))

    res = []
    for i in range(min(n, len(sentences))):
        res.append(sentenceScore[i][0])

    return res



    #raise NotImplementedError


if __name__ == "__main__":
    main()
