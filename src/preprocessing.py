'''
Fitler out undersired characters & words
'''
import re


class RegxFilter:
    def __init__(self, pattern):
        self.pattern = re.compile(r"{}".format(pattern), flags=re.MULTILINE)

    def preprocess(self, text, sub=' '):
        return self.pattern.sub(sub, text)


def clean_text_line(text_line, length_threshold=1):
    '''Remove digits, special characters, excess whitespace & too short tokens

    Parameters
    ----------
    text_line : list
        one line of text (list of tokens)
    length_threshold : int, optional
        remove tokens shorter or equal to, by default 1

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

            if token_:
                text_line_.append(token_)

    return text_line_


def preprocess_file(file):

    for block in file:
        block['content'] = [clean_text_line(
            line) for line in block['content'] if clean_text_line(line)]

    return file
