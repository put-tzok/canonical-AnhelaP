#! /usr/bin/python3
import glob
import json
import logging
import os.path
import unittest
import sys


class DotBracket:
    '''
    RNA structure in dot-bracket notation.

    Attributes:
        sequence (str):     Nucleotide sequence.
        structure (str):    A string of dots and brackets.
        pairs (list):       A list of pairs e.g. [(0, 120), (1, 119), ...] parsed from `structure` attribute.
    '''

    @staticmethod
    def from_string(sequence, structure):
        # TODO: implement this
        pairs = []
        return DotBracket(sequence, structure, pairs)

    def __init__(self, sequence, structure, pairs):
        self.sequence = sequence
        self.structure = structure
        self.pairs = pairs

    def to_bpseq(self):
        '''
        Prepare a list of entries i.e. [(1, 'G', 121), (2, 'A', 120), (3, 'U', 0), ...] and create BPSEQ instance.

        Returns:
            BPSEQ:      An instance of BPSEQ object created from this object.
        :return:
        '''
        # TODO: implement this
        entries = []
        return BPSEQ(entries)


class BPSEQ:
    '''
    RNA structure.

    Attributes:
        entries (tuple):    A list of triples (i, s, j), where 'i' is the nucleotide index (starting from 1),
                            's' is a character in sequence and `j` is the index of paired nucleotide (or zero if
                            unpaired)
    '''

    @staticmethod
    def from_file(bpseq_path):
        '''
        Read a BPSEQ file and parse its content.

        Parameters:
            bpseq_path (str):   Path to a BPSEQ file.

        Returns:
            BPSEQ:              An instance of this class.
        '''
        entries = []
        with open(bpseq_path) as fd:
            for line in fd:
                fields = line.strip().split()
                if len(fields) != 3:
                    logging.warning('Failed to find 3 columns in BPSEQ line: {}', line)
                    continue
                entry = (int(fields[0]), fields[1], int(fields[2]))
                entries.append(entry)
        return BPSEQ(entries)

    def __init__(self, entries):
        self.entries = tuple((i, c, j) for i, c, j in entries)

    def __str__(self):
        return '\n'.join(('{} {} {}'.format(i, c, j) for i, c, j in self.entries))

    def __eq__(self, other):
        return len(self.entries) == len(other.entries) and all(ei == ej for ei, ej in zip(self.entries, other.entries))


def generate_test_function(json_path):
    def test_function():
        with open(json_path) as json_file:
            data = json.load(json_file)
        sequence = ''.join(data['dbn']['all_chains']['bseq'].split('&'))
        structure = ''.join(data['dbn']['all_chains']['sstr'].split('&'))
        dot_bracket = DotBracket.from_string(sequence, structure)
        bpseq1 = dot_bracket.to_bpseq()

        bpseq_path = json_path.replace('.json', '.bpseq')
        bpseq2 = BPSEQ.from_file(bpseq_path)
        assert bpseq1 == bpseq2

    test_function.__name__ = 'test_{}'.format(os.path.basename(json_path))
    return test_function


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for json_path in glob.iglob('data/????.json'):
        suite.addTest(unittest.FunctionTestCase(generate_test_function(json_path)))
    unittest.TextTestRunner().run(suite)
