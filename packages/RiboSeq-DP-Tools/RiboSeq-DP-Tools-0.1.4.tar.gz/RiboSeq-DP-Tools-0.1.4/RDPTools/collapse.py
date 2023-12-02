import gzip
from Bio.SeqIO.QualityIO import FastqGeneralIterator

def fill_template(template: str, read: str, count: str) -> str:
    '''
    Replace the placeholders in the template with the provided values

    Args:
        template (str): Template string
        read (int): Read number
        count (int): Number of times the read was observed

    Returns:
        str: Formatted string
    '''
    if "READ" not in template or "COUNT" not in template:
        raise ValueError("Template must contain READ and COUNT placeholders")
    elif template.count("READ") > 1 or template.count("COUNT") > 1:
        raise ValueError("Template must contain only one READ and COUNT placeholder")
    elif template.split('READ')[0].strip('>') == template.split('READ')[1].split('COUNT')[0]:
        raise ValueError(f"Template ({template}) read and count must have unique delimiters")

    return template.replace("READ", read).replace("COUNT", count)


def collapse(infile: str, outfile: str, format=f">seqREAD_xCOUNT") -> None:
    '''
    Collapse identical reads and return a fasta file with the collapsed reads

    Output header takes the format of ">seqREAD_xCOUNT" where READ is the read 
    number and COUNT is the number of times the read was observed

    To provide a custom header format, use the format argument including READ and COUNT
    as placeholders for the read number and count respectively. Everything before 

    Args:
        infile (str): Path to the input fasta file (can be gzipped)
        outfile (str): Path to the output fasta file
        format (str, optional): Custom header format. Defaults to ">seqREAD_xCOUNT".
    
    Returns:
        None
    '''
    if ">" not in format:
        raise ValueError("Header format must contain '>' character")
    
    unique_reads = {}

    # handle gzipped files
    with open(infile, 'rb') as f:
        magic_number = f.read(2)
        if magic_number == b'\x1f\x8b':
            f = gzip.open(infile, 'rt')
        else:
            f.seek(0)
            f = open(infile, 'r')

        # iterate over the input file recording the number of times each sequence is observed
        print(f"Reading input file {infile}...")
        for title, sequence, quality in FastqGeneralIterator(f):
            if sequence in unique_reads:
                unique_reads[sequence]['count'] += 1
            else:
                unique_reads[sequence] = {}
                unique_reads[sequence]['count'] = 1

    # write the collapsed reads to the output file using the provided header format
    if outfile.endswith('.gz'):
        f = gzip.open(outfile, 'wt')
    else:
        f = open(outfile, 'w')

    read_number = 1
    for seq, vals in unique_reads.items():
        f.write(f"{fill_template(format, str(read_number), str(vals['count']))}\n")
        f.write(f"{seq}\n")
        read_number += 1