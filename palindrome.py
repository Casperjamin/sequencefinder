#!/usr/bin/env python3
import sys
from sequencefinder import reverse_complement
from itertools import combinations_with_replacement 
from argparse import ArgumentParser

def generate_palindromes(length):
    sys.stderr.write(f'generating palindromes for length {length}\n')
    if length % 2 != 0:
        print('length is not even, therefore no palindrome can be generated')
        sys.exit(1)
    
    baseseq = combinations_with_replacement('ACGT', int(length / 2))

    for i in baseseq:
        i  = "".join(i)
        print(i + reverse_complement(i))


def main(command_line = None):
    parser = ArgumentParser(description = 'Generate list of palindrome sequences')
    parser.add_argument("-s",
        required = True,
        dest = "seq",
        type = int,
        help = 'length sequence to generate palindromes for')

    args = parser.parse_args(command_line)
    # launch
    generate_palindromes(args.seq)

if __name__ == "__main__":
    main()
