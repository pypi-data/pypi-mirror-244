# RDP-Tools

[![PyPI Version](https://img.shields.io/pypi/v/RiboSeq-DP-Tools.svg)](https://pypi.python.org/pypi/RiboSeq-DP-Tools)
[![Documentation Status](https://readthedocs.org/projects/RiboSeq-DP-Tools/badge/?version=latest)](https://RiboSeq-DP-Tools.readthedocs.io/en/latest/?version=latest)

A Python command-line utility for programmatically interacting with RiboSeq.Orgs Data Portal.

- Free software: MIT license
- Documentation: [https://RDP-Tools.readthedocs.io](https://RDP-Tools.readthedocs.io)

## Installation

Install RDP-Tools by running:

```bash
pip install RiboSeq-DP-Tools
```
or:
```bash
docker pull quay.io/jackcurragh/rdp-tools
```


## Usage

RDP-Tools is intended to be used as a command line tool.

To collapse a FASTQ file, run:

```bash
RDP-Tools collapse <input_FASTQ>
```

To inflate a FASTA file, run:

```bash
RDP-Tools inflate <input_FASTA>
```

To inflate a FASTA to a FASTQ file, run:
   
```bash
RDP-Tools inflate <input_FASTA> -o <output_file>.fastq/fq
```

To inflate a BAM file, run:
      
```bash
RDP-Tools inflate <input_BAM>
```

For more information on how to use RDP-Tools, see the documentation_ or use :code:`--help`

documentation: https://rdp-tools.readthedocs.io/en/latest/?version=latest


