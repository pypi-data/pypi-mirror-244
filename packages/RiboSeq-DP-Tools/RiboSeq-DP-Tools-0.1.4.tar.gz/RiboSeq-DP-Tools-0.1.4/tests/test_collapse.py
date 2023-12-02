
from RDPTools.collapse import collapse

import gzip
import hashlib
import pytest


def test_collapse_fq():
    collapse(
        'tests/test_data/reads.fq',
        'tests/test_data/reads.collapsed.fa',
    )
    with open('tests/test_data/reads.collapsed.fa', 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        assert m.hexdigest() == '1d2cc643a8ca7642e68964fae580b56b'

def test_collapse_fq_gz():
    collapse(
        'tests/test_data/reads.fq.gz',
        'tests/test_data/reads.collapsed.fa.gz',
    )
    # these files must be read differently as gzip files from python automatically
    # add the metadata (no -n flag) so MD5 hashes will not match
    with gzip.open('tests/test_data/reads.collapsed.fa.gz', 'rb') as f:
        content = f.read()
    
    md5_hash = hashlib.md5(content).hexdigest()
    assert md5_hash == '1d2cc643a8ca7642e68964fae580b56b'

def test_collapse_format():
    collapse(
        'tests/test_data/reads.fq',
        'tests/test_data/reads.collapsed.fa',
        format='>testREAD_xCOUNT',
    )
    with open('tests/test_data/reads.collapsed.fa', 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        assert m.hexdigest() == 'bb860f18c24e3a1278acd6a09f6103b8'

def test_collapse_error_raised_unqi_delims():
    with pytest.raises(ValueError, match="read and count must have unique delimiters"):
        collapse(
            'tests/test_data/reads.fq',
            'tests/test_data/reads.collapsed.fa',
            format='>testREADtestCOUNT',
        )
        with open('tests/test_data/reads.collapsed.fa', 'rb') as f:
            m = hashlib.md5()
            m.update(f.read())

def test_collapse_error_raised_missing_delim():
    with pytest.raises(ValueError, match="Template must contain READ and COUNT placeholders"):
        collapse(
            'tests/test_data/reads.fq',
            'tests/test_data/reads.collapsed.fa',
            format='>testtestCOUNT',
        )
        with open('tests/test_data/reads.collapsed.fa', 'rb') as f:
            m = hashlib.md5()
            m.update(f.read())

def test_collapse_error_raised_double_read():
    with pytest.raises(ValueError, match="Template must contain only one READ and COUNT placeholder"):
        collapse(
            'tests/test_data/reads.fq',
            'tests/test_data/reads.collapsed.fa',
            format='>testREADtestCOUNT_READ',
        )
        with open('tests/test_data/reads.collapsed.fa', 'rb') as f:
            m = hashlib.md5()
            m.update(f.read())