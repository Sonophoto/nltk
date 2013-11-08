"""
See `<http://programminghistorian.org/lessons/topic-modeling-and-mallet>`_

>>> data = import_dir('docs')

>>> train_topics(data) #output keywords

>>> train_topics(data, num_topics=20, optimize_interval=20, output_state='topic-state.gz', output_topic_keys='tutorial_keys.txt', output_doc_topics='tutorial_compostion.txt')
    
    




"""
from tempfile import mkstemp


_FIND_TOPICS = "cc.mallet.fst.SimpleTagger"

def import_dir(directory):
    (fd, data_file) = mkstemp('.txt', 'train')
    pass

def train_topics(data, num_topics=100, optimize_interval=0,
                 output_state=None, output_topic_keys=None, output_doc_topics=None, trace=1):
    
    (fd,  model_file) = mkstemp('.txt', 'topic_model')
    
    if trace >= 1:
        print('[MalletCRF] Calling mallet to train CRF...')
        
    cmd = [_FIND_TOPICS, '--train', 'true',
                   '--model-file', os.path.abspath(filename), data]


def parse_mallet_output(s):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
