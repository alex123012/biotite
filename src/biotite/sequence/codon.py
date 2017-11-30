# Copyright 2017 Patrick Kunzmann.
# This source code is part of the Biotite package and is distributed under the
# 3-Clause BSD License.  Please see 'LICENSE.rst' for further information.

import copy
from os.path import join, dirname, realpath
from .sequence import Sequence
from .seqtypes import NucleotideSequence, ProteinSequence

__all__ = ["CodonTable"]


class CodonTable(object):
    
    # file for codon datbles
    _table_file = join(dirname(realpath(__file__)), "codon_tables.txt")
    
    def __init__(self, codon_dict, starts):
        self._symbol_dict = copy.copy(codon_dict)
        self._code_dict = {}
        for key, value in self._symbol_dict.items():
            key_code = tuple(Sequence.encode(key, NucleotideSequence.alphabet))
            val_code = ProteinSequence.alphabet.encode(value)
            self._code_dict[key_code] = val_code
        self._start_symbols = tuple((starts))
        self._start_codes = tuple(
            [tuple(Sequence.encode(start, NucleotideSequence.alphabet))
             for start in self._start_symbols]
        )
        
    def codon_dict(self, code=False):
        if code:
            return copy.copy(self._code_dict)
        else:
            return copy.copy(self._symbol_dict)
    
    def start_codons(self, code=False):
        if code:
            return self._start_codes
        else:
            return self._start_symbols
    
    @staticmethod
    def load(table_name):
        # Loads a codon table from codon_tables.txt
        with open(CodonTable._table_file, "r") as f:
            lines = f.read().split("\n")
        
        # Extract data for codon table from file
        table_found = False
        aa = None
        init = None
        base1 = None
        base2 = None
        base3 = None
        for line in lines:
            if not line:
                table_found = False
            if type(table_name) == int and line.startswith("id"):
                # remove identifier 'id'
                if table_name == int(line[2:]):
                    table_found = True
            elif type(table_name) == str and line.startswith("name"):
                # Get list of table names from lines
                # (separated with ';')
                # remove identifier 'name'
                names = [name.strip() for name in line[4:].split(";")]
                if table_name in names:
                    table_found = True
            if table_found:
                if line.startswith("AA"):
                    #Remove identifier
                    aa = line[5:].strip()
                elif line.startswith("Init"):
                    init = line[5:].strip()
                elif line.startswith("Base1"):
                    base1 = line[5:].strip()
                elif line.startswith("Base2"):
                    base2 = line[5:].strip()
                elif line.startswith("Base3"):
                    base3 = line[5:].strip()
        
        # Create codon tbale from data
        if aa is not None and init is not None \
            and base1 is not None and base2 is not None and base3 is not None:
                symbol_dict = {}
                starts = []
                # aa, init and baseX all have the same length
                for i in range(len(aa)):
                    codon = base1[i] + base2[i] + base3[i]
                    if init[i] == "i":
                        starts.append(codon)
                    symbol_dict[codon] = aa[i]
                return CodonTable(symbol_dict, starts)
        else:
            raise ValueError("Codon table '{:}' was not found"
                             .format(str(table_name)))
    
    @staticmethod
    def default_table():
        return _default_table

_std_table = CodonTable.load("Standard")
_default_table = CodonTable(_std_table.codon_dict(), ["ATG"])
    
    