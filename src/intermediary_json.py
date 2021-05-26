# %%
import re
from collections import OrderedDict

import xmltodict


# %%
# with open('../data/raw/aarhusstiftstidende-1946-03-31-01-0537A.alto.xml') as fin:
#     doc = xmltodict.parse(fin.read())


# def maximal_extraction(doc):
#     '''
#     In progress
#     Content missing
#     '''
#     return {
#         'date': None,
#         'page_id': None,
#         'source_image': doc['alto']['Description']['sourceImageInformation']['fileName'],
#         'paragraph_styles': doc['alto']['Styles']['ParagraphStyle'],
#         'text_styles': doc['alto']['Styles']['TextStyle'],
#     }

# # %%
# doc['alto']['Layout']['Page']['PrintSpace']['TextBlock'][0]['TextLine']

# # %%
# doc['alto']['Layout']['Page']['PrintSpace']['TextBlock'][0]['TextLine']['String'][0]

# # %%
# xml_text_blocks = doc['alto']['Layout']['Page']['PrintSpace']['TextBlock']

# %%
# WORKING HERE

def extract_line_content(line_content):

    if isinstance(line_content, OrderedDict):
        text = [line_content['@CONTENT']]

    elif isinstance(line_content, list):
        text = [obj['@CONTENT'] for obj in line_content]
    
    return text

def extract_block(block):
    block_text = []

    if 'TextLine' in block:
        xml_text_lines = block['TextLine']

        # in case of single line
        block_text = []
        if isinstance(xml_text_lines, OrderedDict):
            line_content = xml_text_lines['String']
            text = extract_line_content(line_content)
            block_text.append(text)

        # in case of many lines
        elif isinstance(xml_text_lines, list):
            line_text = []
            for line in xml_text_lines:
                line_content = line['String']
                text = extract_line_content(line_content)
                line_text.append(text)
            block_text.extend(line_text)
    
    return block_text


# each block has to be a json object
def block_to_json(block, fname):

    pattern_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    pattern_page = re.compile(r'(?<=\d{4}-\d{2}-\d{2}-\d{2}-).*(?=\.jp2)')

    date = pattern_date.search(fname).group(0)
    page_id = pattern_page.search(fname).group(0)
    source_img = fname
    content = extract_block(block)

    return {
        'date': date,
        'page_id': page_id,
        'source_img': source_img,
        'content': content
    }


def parse_file(doc):

    fname = doc['alto']['Description']['sourceImageInformation']['fileName']
    try:
        xml_text_blocks = doc['alto']['Layout']['Page']['PrintSpace']['TextBlock']

        # in case the document only has one text block
        if isinstance(xml_text_blocks, OrderedDict):
            xml_text_blocks = [xml_text_blocks]

    except KeyError:
        xml_text_blocks = None

    out = []
    if xml_text_blocks:
        for block in xml_text_blocks:
            out.append(block_to_json(block, fname))
    
    return out

# %%
faulty_paths = [
    '/media/jan/Seagate Expansion Drive/stiftstidende/1932-46/B400026954450-RT2/400026954450-03/1933-06-25-01/aarhusstiftstidende-1933-06-25-01-0553A.alto.xml'
]

with open(faulty_paths[0]) as fin:
    doc = xmltodict.parse(fin.read())

a = doc['alto']['Layout']['Page']['PrintSpace']['TextBlock']


doc_ = parse_file(doc)

# %%

