# Natural Language Toolkit: Twitter Corpus Reader
#
# Copyright (C) 2001-2013 NLTK Project
# Author: Ewan Klein <ewan@inf.ed.ac.uk>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
A reader for corpora that consist of tweets.
"""

import codecs
import json

from nltk import compat
import nltk.data
from nltk.tokenize import *

from nltk.corpus.reader.util import *
from nltk.corpus.reader.api import *


class TweetCorpusReader(CorpusReader):
    """
    Reader for corpora that consist of Tweets stored as serialized JSON objects.  
    Sentences and words can
    be tokenized using the default tokenizers, or by custom tokenizers
    specified as parameters to the constructor.
    """

    CorpusView = StreamBackedCorpusView
    """The corpus view class used by this reader.  Subclasses of
       ``TweetCorpusReader`` may specify alternative corpus view
       classes (e.g., to skip the preface sections of documents.)"""

    def __init__(self, root="", fileids="",
                 word_tokenizer=WordPunctTokenizer(),
                 sent_tokenizer=nltk.data.LazyLoader(
                     'tokenizers/punkt/english.pickle'),
                 #para_block_reader=read_blankline_block,
                 encoding='utf8'):
        """
        Construct a new plaintext corpus reader for a set of documents
        located at the given root directory.  Example usage:

            >>> root = '/usr/local/share/nltk_data/corpora/webtext/'
            >>> reader = PlaintextCorpusReader(root, '.*\.txt') # doctest: +SKIP

        :param root: The root directory for this corpus.
        :param fileids: A list or regexp specifying the fileids in this corpus.
        :param word_tokenizer: Tokenizer for breaking sentences or
            paragraphs into words.
        :param sent_tokenizer: Tokenizer for breaking tweets
            into sentences.
  
        """
        CorpusReader.__init__(self, root, fileids, encoding)
        self._word_tokenizer = word_tokenizer
        self._sent_tokenizer = sent_tokenizer

        
    def tweets(self, fileids=None):
        """
        :return: the given file(s) as a single string.
        :rtype: str
        """
        #if fileids is None: fileids = self._fileids
        #elif isinstance(fileids, compat.string_types): fileids = [fileids]
        #return concat([self.open(f).read() for f in fileids])
        
        tweets = [json.loads(line) for line in open('collection.json')]
        return [json.dumps(tweet, indent=4, sort_keys=True) for tweet in tweets]
            
    def text(self, fileids=None):
        """
        :return: the given file(s) as a single string.
        :rtype: str
        """
        #if fileids is None: fileids = self._fileids
        #elif isinstance(fileids, compat.string_types): fileids = [fileids]
        #return concat([self.open(f).read() for f in fileids])
        tweets = [json.loads(line) for line in  open('collection.json')]
       
        return [tweet['text'] for tweet in tweets]

    def words(self, fileids=None):
        """
        :return: the given file(s) as a list of words
            and punctuation symbols.
        :rtype: list(str)
        """
        return concat([self.CorpusView(path, self._read_word_block, encoding=enc)
                       for (path, enc, fileid)
                       in self.abspaths(fileids, True, True)])

    def sents(self, fileids=None):
        """
        :return: the given file(s) as a list of
            sentences or utterances, each encoded as a list of word
            strings.
        :rtype: list(list(str))
        """
        if self._sent_tokenizer is None:
            raise ValueError('No sentence tokenizer for this corpus')

        return concat([self.CorpusView(path, self._read_sent_block, encoding=enc)
                       for (path, enc, fileid)
                       in self.abspaths(fileids, True, True)])

    def paras(self, fileids=None):
        """
        :return: the given file(s) as a list of
            paragraphs, each encoded as a list of sentences, which are
            in turn encoded as lists of word strings.
        :rtype: list(list(list(str)))
        """
        if self._sent_tokenizer is None:
            raise ValueError('No sentence tokenizer for this corpus')

        return concat([self.CorpusView(path, self._read_para_block, encoding=enc)
                       for (path, enc, fileid)
                       in self.abspaths(fileids, True, True)])

    def _read_word_block(self, stream):
        words = []
        for i in range(20): # Read 20 lines at a time.
            words.extend(self._word_tokenizer.tokenize(stream.readline()))
        return words

    def _read_sent_block(self, stream):
        sents = []
        for para in self._para_block_reader(stream):
            sents.extend([self._word_tokenizer.tokenize(sent)
                          for sent in self._sent_tokenizer.tokenize(para)])
        return sents

    def _read_para_block(self, stream):
        paras = []
        for para in self._para_block_reader(stream):
            paras.append([self._word_tokenizer.tokenize(sent)
                          for sent in self._sent_tokenizer.tokenize(para)])
        return paras


    
if __name__ == '__main__':
    tr = TweetCorpusReader()
    for t in tr.raw(): 
        print(t) 
    print()
    for t in tr.text():
        print(t)
