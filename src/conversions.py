'''
Convert file format from intermediary json to X
'''

# TXT


def doc_to_txt(file, word_sep=' ', line_sep='\n', block_sep='\n\n') -> str:
    text_page = []
    for block in file:
        text_line = []
        for line in block['content']:
            one_line = word_sep.join(line)
            text_line.append(one_line)
        text_block = line_sep.join(text_line)
        text_page.append(text_block)

    text_page = block_sep.join(text_page)

    return text_page


def export_txt(file, outpath, file_sep='\n\n\n\n') -> None:
    if file_sep:
        file = file_sep.join(file)
    with open(outpath, 'w') as fout:
        fout.write(file)
