import re


multistream_reg = re.compile('multistream')
pages_full_reg = re.compile('pages-articles')
pages_reg = re.compile('pages-articles[1-9]')


def validate_file(filename, is_full):
    """We should only download files with pages-articles substing in name"""
    multistream = multistream_reg.findall(filename)
    article_pattern = pages_full_reg if is_full else pages_reg
    article = article_pattern.findall(filename)
    if not multistream and article:
        return True
    return False