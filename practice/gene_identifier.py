"""
In this made up example world that is an extremely simplified version of reality, DNA is represented as a string made up
of characters from the set {A, C, T, G} (representing the four nucleotides in real life DNA).
A "gene" is a specific, well known DNA sequence that relates to a particular function or characteristic of an organism.
Additionally, the example world scientific community uses unique string identifiers for each gene, such as
"growth-gene-1" or "immunity-gene-46".

Identifying genes in long sequences of DNA is a computationally intense process, made more difficult by naturally
occurring random mutations in DNA. This code shows an object-oriented design for searching a DNA sequence for
genes.
"""
from abc import ABC, abstractmethod
from collections.abc import *

import textdistance
import json


class GeneIdentifier(ABC):

    @abstractmethod
    def identify(self, dna_sequence: str) -> Iterable[str]:
        """
        Given a DNA sequence (a string containing the base pair characters A, C, T, and G), identify any gene(s)
        present in the string.

        :param dna_sequence: The sequence of base pairs as a Python string.
        :return: An iterable of strings representing the IDs of genes.
        """
        pass


class DictionaryGeneIdentifier(GeneIdentifier, ABC):
    """
    Gene identifier using a dictionary of gene sequence to gene name.
    """

    def __init__(self, gene_dictionary: Mapping[str, str]):
        """

        :param gene_dictionary: Mapping of {sequence: gene_name}
        """
        self.gene_dictionary = gene_dictionary

    @staticmethod
    def from_json_file(filename, search_type="exact"):
        """
        Static factory method to create a dictionary-based gene identifier from a JSON file describing the dictionary.
        :param filename: JSON filename.
        :param search_type: Type of search desired: "exact" or "fuzzy"
        :return:
        """
        with open(filename, "r") as f:
            gene_dict = json.load(f)
        if search_type == "exact":
            return ExactGeneIdentifier(gene_dict)
        else:
            return BruteForceFuzzyGeneIdentifier(gene_dict)


class ExactGeneIdentifier(DictionaryGeneIdentifier):

    def __init__(self, gene_dictionary: Mapping[str, str]):
        """

        :param gene_dictionary: Mapping of {sequence: gene_name}
        """
        super(ExactGeneIdentifier, self).__init__(gene_dictionary)

    def identify(self, dna_sequence) -> Iterable[str]:
        """
        Identify the genes present by looking them up in a dictionary and finding an exact match.
        :param dna_sequence:
        :return:
        """
        genes = set()
        for gene_seq, gene_name in self.gene_dictionary.items():
            if dna_sequence.find(gene_seq) >= 0:
                genes.add(gene_name)
        return genes


class BruteForceFuzzyGeneIdentifier(DictionaryGeneIdentifier):
    """
    Searches for inexact but close matches, thus attempting to account for mutations in gene sequences
    """

    def __init__(self, gene_dictionary: Mapping[str, str]):
        """

        :param gene_dictionary: Mapping of {sequence: gene_name}
        """
        super(BruteForceFuzzyGeneIdentifier, self).__init__(gene_dictionary)

    def identify(self, dna_sequence) -> Iterable[str]:
        """
        Uses Levenshtein distance to find substrings that are similar to the dictionary genes.
        :param dna_sequence:
        :return:
        """
        genes = set()
        for gene_seq, gene_name in self.gene_dictionary.items():
            # not so efficient levenshtein search that looks at every possible substring with the same length as the
            # gene
            for i in range(0, len(dna_sequence) - len(gene_seq)):
                # Levenshtein
                if textdistance.levenshtein(gene_seq, dna_sequence[i:i + len(gene_seq)]) < 3:
                    genes.add(gene_name)
        return genes

# TODO More efficient, B-tree style Leveshtein search such as in:
# https://github.com/mattandahalfew/Levenshtein_search/blob/master/Lev_search.c
