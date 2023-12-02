
from RDPTools.inflate import inflate_fasta, inflate_bam
import gzip
import hashlib
import pysam
import pytest


def test_inflate_bam():
    infile = 'tests/test_data/test.bam'
    outfile = 'tests/test_data/test.inflated.bam'
    inflate_bam(infile, outfile)
    pysam.index(outfile)
    bam = pysam.AlignmentFile(outfile, 'rb')
    assert bam.count() == 158312

def test_inflate_fasta():
    inflate_fasta(
        'tests/test_data/reads.collapsed.fa.gz',
        'tests/test_data/test.inflated.fa')
    with open('tests/test_data/test.inflated.fa', 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        assert m.hexdigest() == 'b36b91d8eb1b407324ffa0c6fa50f8e6'

def test_inflate_fasta_gz():
    inflate_fasta(
        'tests/test_data/reads.collapsed.fa.gz',
        'tests/test_data/test.inflated.fa.gz',
        compress=True)
    # these files must be read differently as gzip files from python automatically
    # add the metadata (no -n flag) so MD5 hashes will not match
    with gzip.open('tests/test_data/test.inflated.fa.gz', 'rb') as f:
        content = f.read()
    
    md5_hash = hashlib.md5(content).hexdigest()
    assert md5_hash == 'b36b91d8eb1b407324ffa0c6fa50f8e6'

def test_inflate_fasta_to_fastq():
    infile = 'tests/test_data/reads.collapsed.fa'
    outfile = 'tests/test_data/test.inflated.fq'
    inflate_fasta(infile, outfile)
    with open(outfile, 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        assert m.hexdigest() == 'd41d8cd98f00b204e9800998ecf8427e'

def test_inflate_fasta_to_fastq_gz():
    inflate_fasta(
        'tests/test_data/reads.collapsed.fa.gz',
        'tests/test_data/test.inflated.fq.gz',
        compress=True)

    with gzip.open('tests/test_data/test.inflated.fq.gz', 'rb') as f:
        content = f.read()
    
    md5_hash = hashlib.md5(content).hexdigest()
    assert md5_hash == 'ed038e7ec59fa7b5504832c0b505d071'
