'''
Concatenate content from intermediary json to timebins of desired length

Must be OS agnostic
'''
# %%
import os
import re
import glob
import argparse

import ndjson
import pandas as pd
from tqdm import tqdm

from conversions import doc_to_txt, export_txt

# %%
def extract_date(fname):
    pattern_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    date = pattern_date.search(fname).group(0)

    return date

def extract_simple_fname(group_name):
    if group_name.freq == 'Y':
        return group_name.strftime('%Y')

    elif group_name.freq == 'M':
        return group_name.strftime('%Y-%m')

    elif group_name.freq == 'D':
        return group_name.strftime('%Y-%m-%d')

    else:
        raise ValueError(f'Timestamp frequency not recognized ({group_name.freq})')


# %%
# pd df
# pages must be sorted
def group_paths(intermediary_pattern, freq='D'):

    paths = sorted(glob.glob(intermediary_pattern))

    dates = [extract_date(fname) for fname in paths]
    assert len(dates) == len(paths)


    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'path': paths
    })

    return df.groupby(pd.Grouper(key='date', axis=0, freq=freq))


# %%
def bin_it(df_group, outdir, conversion_func=doc_to_txt, export_func=export_txt):
    '''
    '''
    for name, group in tqdm(df_group):
        group_output = []

        # iterate thourgh paths in that group
        paths = [path for path in group['path']]
        for path in paths:
            with open(path) as fin:
                file = ndjson.load(fin)

            # format page with selected parser
            file_ = conversion_func(file)
            # collect in a single object for exporting
            # except for empties
            if file_:
                group_output.append(file_)
        
        # use name as fname
        group_start_date = name.strftime('%Y-%m-%d')
        fname = f'{group_start_date}_{name.freqstr}'
        outpath = os.path.join(outdir, fname)
        # export group output
        export_func(group_output, outpath)



if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Extract Stiften with desired properities")
    ap.add_argument("-d", "--dataset", required=True, help="path to intermediary json files")
    ap.add_argument("-o", "--outdir", required=True, help="path to directory to which files will be extracted")
    ap.add_argument("-f", "--format", required=False, type=str, default='txt', help="desired format")
    ap.add_argument('-t', '--timebin', required=False, type=str, default='D', help='time bins of this frequency')
    args = vars(ap.parse_args())

    # intermediary_root = '/home/jan/Documents/_git/alto-tools/data/processed/json'
    intermediary_pattern = os.path.join(args['dataset'], '*', '*', '*', '*.ndjson')
    df_group = group_paths(intermediary_pattern, args['timebin'])

    if not os.path.exists(args['outdir']):
        os.mkdir(args['outdir'])

    if args['format'] == 'txt':
        bin_it(
            df_group=df_group,
            outdir=args['outdir'],
            conversion_func=doc_to_txt,
            export_func=export_txt
            )
