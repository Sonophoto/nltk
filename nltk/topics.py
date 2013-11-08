"""
See `<http://programminghistorian.org/lessons/topic-modeling-and-mallet>`_

>>> data = import_dir('docs')

>>> train_topics(data) #output keywords

>>> train_topics(data, num_topics=20, optimize_interval=20, output_state='topic-state.gz', output_topic_keys='tutorial_keys.txt', output_doc_topics='tutorial_compostion.txt')
    
    




"""
import os
from tempfile import mkstemp

from nltk.classify import call_mallet

_INPUT_DIR = 'cc.mallet.classify.tui.Text2Vectors'

_TRAIN_TOPICS = "cc.mallet.topics.tui.Vectors2Topics"

def import_dir(directory, trace=1):
    
    if trace >= 1:
        print('[MalletLDA] Calling mallet to convert input directory: %s' %
              directory)
        
    cmd = [_INPUT_DIR, '--input', os.path.abspath(directory)]
    call_mallet(cmd)

def train_topics(data, num_topics=100, optimize_interval=0,
                 output_state=None, output_topic_keys=None, output_doc_topics=None, trace=1):
    
    (fd,  model_file) = mkstemp('.txt', 'topic_model')
    
    if trace >= 1:
        print('[MalletLDA] Calling mallet to train topics from %s')
        
    cmd = [_FIND_TOPICS, '--train', 'true',
                   '--model-file', os.path.abspath(filename), data]


def parse_mallet_output(s):
    pass


if __name__ == "__main__":
    
    _mallet_home = os.environ.get('MALLET')
    data_dir = os.path.join(_mallet_home, 'sample-data/web/en')
    data = import_dir(data_dir)
    
    #import doctest
    #doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
