'''
Find legit files to extract XML from

stiftstidene_root
-----------------
    +-- Session *-RT{\d}
    |   +-- Subsesion {\d{15}}
    |   |   +-- Daily folder {YYYY-MM-DD}
    |   |   |   +-- Page file {*.alto.xml}
'''
# %%
import os
import re

import ndjson
import xmltodict
from tqdm import tqdm

from intermediary_json import parse_file


# %%
def get_sessions_paths(parent_dir, absolute=True):
    subpaths_all = [d for d in os.listdir(parent_dir)]
    subpaths_dir = [d for d in subpaths_all 
            if os.path.isdir(os.path.join(parent_dir, d))]
    
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
    subpaths_dailydir = [d for d in subpaths_dir if re.match(pattern_dailydir, d)]

    if absolute:
        return [os.path.join(parent_dir, d) for d in subpaths_dailydir]
    else:
        return subpaths_dailydir


def get_xml_paths(parent_dir, absolute=True):
    subpaths_xml = [f for f in os.listdir(parent_dir) if f.endswith('.alto.xml')]

    if absolute:
        return [os.path.join(parent_dir, d) for d in subpaths_xml]
    else:
        return subpaths_xml


# # %%
# a = get_subsession_paths(pahts_1[0])
# b = get_dailydir_paths(a[0])
# c = get_xml_paths(b[0])

# %%
def make_folder_structure(dataset_root, target_dir):
    os.mkdir(target_dir)

    sessions = get_sessions_paths(dataset_root)
    for i, session in enumerate(sessions):
        out_session = os.path.join(target_dir, os.path.basename(session))
        os.mkdir(out_session)

        subsessions = get_subsession_paths(session)
        print(f'session {i} of out {len(sessions)}')
        for i, subsession in enumerate(subsessions):
            out_subsession = os.path.join(out_session, os.path.basename(subsession))
            os.mkdir(out_subsession)

            dailydirs = get_dailydir_paths(subsession)
            print(f'subsession {i} of out {len(subsessions)}')
            for dailydir in tqdm(dailydirs):
                out_dailydir = os.path.join(out_subsession, os.path.basename(dailydir))
                os.mkdir(out_dailydir)

                xml_paths = get_xml_paths(dailydir)
                for file in xml_paths:
                    out_xml = os.path.join(
                        out_dailydir, os.path.basename(file).replace('.alto.xml', '.ndjson')
                        )

                    with open(file) as fin:
                        doc = xmltodict.parse(fin.read())

                    doc_ = parse_file(doc)

                    with open(out_xml, 'w') as fout:
                        ndjson.dump(doc_, fout)


stiftstidene_root = '/media/jan/Seagate Expansion Drive/stiftstidende/1932-46/'
make_folder_structure(
    dataset_root=stiftstidene_root,
    target_dir='/home/jan/Documents/_git/alto-tools/data/processed/json'
)
