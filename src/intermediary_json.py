'''
Find legit files to extract XML from

stiftstidene_root
-----------------
    +-- Session *-RT{\d}
    |   +-- Subsesion {\d{15}}
    |   |   +-- Daily folder {YYYY-MM-DD}
    |   |   |   +-- Page file {*.alto.xml}
'''
import os
import re
import argparse
from collections import OrderedDict

import ndjson
import xmltodict
from tqdm import tqdm
from wasabi import msg


def extract_line_content(line_content):

    # in case of single word in a text line
    if isinstance(line_content, OrderedDict):
        text = [line_content['@CONTENT']]

    # in case of multiple words in a text line
    elif isinstance(line_content, list):
        text = [obj['@CONTENT'] for obj in line_content]

    return text


def extract_block(block):
    block_text = []

    # some text blocks don't have 'TextLine'
    # in that case, empty list is returned
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


def block_to_json(block, fname):
    '''
    Each text block must be a json object,
    so we can track metadata at the highest resolution possible.
    '''

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

    # filename is under this path in every document
    fname = doc['alto']['Description']['sourceImageInformation']['fileName']
    # some documents don't have textblocks
    try:
        xml_text_blocks = doc['alto']['Layout']['Page']['PrintSpace']['TextBlock']

        # in case the document only has one text block
        if isinstance(xml_text_blocks, OrderedDict):
            xml_text_blocks = [xml_text_blocks]

    # document will raise an error if no 'TextBlock'
    except KeyError:
        xml_text_blocks = None

    out = []
    # don't work on empties
    if xml_text_blocks:
        for block in xml_text_blocks:
            out.append(block_to_json(block, fname))

    return out


def get_sessions_paths(parent_dir, absolute=True):
    subpaths_all = [d for d in os.listdir(parent_dir)]
    subpaths_dir = [d for d in subpaths_all
                    if os.path.isdir(os.path.join(parent_dir, d))]

    # check: validate basepath is 17 characters
    subpaths_dir = [d for d in subpaths_dir if len(d) == 17]

    if absolute:
        return [os.path.join(parent_dir, d) for d in subpaths_dir]
    else:
        return subpaths_dir


def get_subsession_paths(parent_dir, absolute=True):
    '''List Subsession paths in a Session directory.
    Subsession path must be a directory with a name of 15 characters.

    Parameters
    ----------
    parent_dir : str
        Path to a Session directory

    absolute : bool, optional
        Return absolute paths or folder names?
        By default True.

    Returns
    -------
    list
        (absolute paths to | names of) subsession dirs
    '''
    subpaths_all = [d for d in os.listdir(parent_dir)]
    subpaths_dir = [d for d in subpaths_all
                    if os.path.isdir(os.path.join(parent_dir, d))]

    # check: validate basepath is 15 characters
    subpaths_ocr = [d for d in subpaths_dir if len(d) == 15]

    if absolute:
        return [os.path.join(parent_dir, d) for d in subpaths_ocr]
    else:
        return subpaths_ocr


def get_dailydir_paths(parent_dir, absolute=True):
    '''List Daily-directory paths in a Subsession directory.
    Daily-directory path must be a directory with a name of {YYYY}-{MM}-{DD}*.

    Parameters
    ----------
    parent_dir : str
        Path to a Subsession directory

    absolute : bool, optional
        Return absolute paths or folder names?
        By default True

    Returns
    -------
    list
        (absolute paths to | names of) daily dirs
    '''
    subpaths_all = [d for d in os.listdir(parent_dir)]
    subpaths_dir = [d for d in subpaths_all
                    if os.path.isdir(os.path.join(parent_dir, d))]

    pattern_dailydir = re.compile(r'\d{4}-\d{2}-\d{2}.*')
    subpaths_dailydir = [
        d for d in subpaths_dir if re.match(pattern_dailydir, d)]

    if absolute:
        return [os.path.join(parent_dir, d) for d in subpaths_dailydir]
    else:
        return subpaths_dailydir


def get_xml_paths(parent_dir, absolute=True):
    subpaths_xml = [f for f in os.listdir(
        parent_dir) if f.endswith('.alto.xml')]

    if absolute:
        return [os.path.join(parent_dir, d) for d in subpaths_xml]
    else:
        return subpaths_xml


def make_folder_structure(dataset_root, target_dir):

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    existing_names_dataset = get_sessions_paths(dataset_root, absolute=False)
    existing_names_target = get_sessions_paths(target_dir, absolute=False)

    sessions = set(existing_names_dataset) - set(existing_names_target)
    sessions = [os.path.join(dataset_root, d) for d in sessions]

    for i, session in enumerate(sessions):
        out_session = os.path.join(target_dir, os.path.basename(session))
        os.mkdir(out_session)

        subsessions = get_subsession_paths(session)
        print(f'session {i} of out {len(sessions)}')
        for i, subsession in enumerate(subsessions):
            out_subsession = os.path.join(
                out_session, os.path.basename(subsession))
            os.mkdir(out_subsession)

            dailydirs = get_dailydir_paths(subsession)
            print(f'subsession {i} of out {len(subsessions)}')
            for dailydir in tqdm(dailydirs):
                out_dailydir = os.path.join(
                    out_subsession, os.path.basename(dailydir))
                os.mkdir(out_dailydir)

                xml_paths = get_xml_paths(dailydir)
                for file in xml_paths:
                    out_xml = os.path.join(
                        out_dailydir, os.path.basename(
                            file).replace('.alto.xml', '.ndjson')
                    )

                    with open(file) as fin:
                        doc = xmltodict.parse(fin.read())

                    doc_ = parse_file(doc)

                    with open(out_xml, 'w') as fout:
                        ndjson.dump(doc_, fout)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Extract Stiften with desired properities")
    ap.add_argument("-d", "--dataset", required=True,
                    help="root directory of stiften datasets (e.g. stiftstidende/1932-46/)")
    ap.add_argument("-o", "--outdir", required=True,
                    help="target dir where intermediary json files are going to get dumped")
    args = vars(ap.parse_args())

    msg.info(f"Starting intermediary json creation with output directory: {args['outdir']}")

    make_folder_structure(
        dataset_root=args['dataset'],
        target_dir=args['outdir']
    )

    msg.good('Job completed: intermediary_json.py')
