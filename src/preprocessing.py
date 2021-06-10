'''
Fitler out undersired characters & words
'''
import re


class RegxFilter:
    def __init__(self, pattern):
        self.pattern = re.compile(r"{}".format(pattern), flags=re.MULTILINE)

    def preprocess(self, text, sub=' '):
        return self.pattern.sub(sub, text)


def load_stopwords(path='mdl/stopord.txt') -> set:
    '''Import stopwords from a txt file (each word = one line)
    '''
    with open(path, encoding='utf-8') as fin:
        stopwords = fin.readlines()

    # get rid of newline characters
    stopwords_ = [RegxFilter(r"\n").preprocess(token, sub='')
                  for token in stopwords]

    return set(stopwords_)


def clean_text_line(text_line, length_threshold=1, stopwords=None):
    '''Remove digits, special characters, excess whitespace & too short tokens

    Parameters
    ----------
    text_line : list
        one line of text (list of tokens)
    length_threshold : int, optional
        remove tokens shorter or equal to, by default 1
    stopwords : set
        set of words to filter out form the datasets. By default None

    Returns
    -------
    list
        filtered line of text (list of tokens)
    '''
    text_line_ = []
    for token in text_line:
        if len(token) > length_threshold:
            token_ = RegxFilter(r"\d+").preprocess(token, sub=' ')
            token_ = RegxFilter(r"\W+").preprocess(token_, sub=' ')
            token_ = RegxFilter(r"\s+").preprocess(token_, sub='')

            if stopwords:
                token_ = token_ if token_ not in stopwords else None

            if token_:
                text_line_.append(token_)

    return text_line_


def preprocess_file(file, **kwargs):
    '''Maximal preprocessing for one json file

    Parameters
    ----------
    file : list of dict
        json file

    Returns
    -------
    list of dict
        preprocessed file
    '''

    for block in file:
        block['content'] = [clean_text_line(
            line) for line in block['content'] if clean_text_line(line, **kwargs)]

    return file
