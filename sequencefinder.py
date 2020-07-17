#!/usr/bin/env python3

from Bio import SeqIO
from argparse import ArgumentParser
import sys

def reverse_complement(sequence):
    revcomp = {
        "A":"T",
        "C":"G",
        "G":"C",
        "T":"A"
    }
    seq = sequence[::-1]
    rev = ""
    for i in seq:
        rev += revcomp[i]
    return rev


def check_seq(seq):
    """check if seq is a valid nucleotide sequence"""
    seq = seq.upper()
    for i in seq:
        if i != 'A' and i != 'C' and i != 'G' and i != 'T':
            print(f'{i} is not a valid nucleotide')
            sys.exit(1)


def read_fasta(fastafile):
    fasta = {}
    for sequence in SeqIO.parse(fastafile, 'fasta'):
        fasta[sequence.id] = str(sequence.seq).upper()
    return fasta


def subsequence_finder(contig, name, seq):
    """ print locations of seq in contig""" 

    rev = reverse_complement(seq)
    length = len(contig) - len(seq) + 1
    for i in range(length):
        kmer = contig[i:i+len(seq)]
        if kmer == seq:
            print(f'{name}\t{i}\t+\t{seq}')
        if kmer == rev:
            print(f'{name}\t{i}\t-\t{seq}')


def analyse_sequence(infasta, seq, cores):
    sys.stderr.write(f'fasta file to check is {infasta}\n')
    sys.stderr.write(f'subsequence: {seq}\n')
    check_seq(seq)
    fasta = read_fasta(infasta)

    for contigname in fasta:
        if seq not in fasta[contigname]:
            continue
        subsequence_finder(fasta[contigname],contigname,  seq)


def main(command_line = None):
    parser = ArgumentParser(description = 'find short subsequences in a fasta')
    parser.add_argument("-i", 
        required = True, 
        dest = "input_file", 
        help = 'sequence in which to look for')

    parser.add_argument("-s",
        required = True,
        dest = "seq", 
        type = str, 
        help = 'subsequence one is looking for')

    parser.add_argument("--cores", 
        required = False, 
        default = 1, 
        type = int,
        dest = 'cores')
    args = parser.parse_args(command_line)
    # launch
    analyse_sequence(args.input_file, args.seq, args.cores)


if __name__ == "__main__":
    main()

