import unittest

from practice import gene_identifier
class GeneIdentifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(clz):
        clz.gene_dict = {
            "CCCCCCCCC": "c-gene-1",
            "CTCTCTCT": "ct-gene-2"
        }

    def test_exact_match(self):
        identifier = gene_identifier.ExactGeneIdentifier(self.gene_dict)
        genes = identifier.identify("ATCGCTCTCTCTGGGAG")
        self.assertEqual({"ct-gene-2"}, genes)

    def test_no_match(self):
        identifier = gene_identifier.ExactGeneIdentifier(self.gene_dict)
        genes = identifier.identify("ACTGACTGACTGACTGACTGACTGACTGACTGACTGACTG")
        self.assertEqual(set(), genes)

    def test_exact_match_multiple(self):
        identifier = gene_identifier.ExactGeneIdentifier(self.gene_dict)
        genes = identifier.identify("ATCGCTCTCTCTGGGAGCCCCCCCCC")
        self.assertEqual({"ct-gene-2", "c-gene-1"}, genes)

    def test_fuzzy_match(self):
        identifier = gene_identifier.BruteForceFuzzyGeneIdentifier(self.gene_dict)
        # Has ct-gene-2 with one mutation (replaced one C with G)
        genes = identifier.identify("ATCGCTCTGTCTGGGAG")
        self.assertEqual({"ct-gene-2"}, genes)

    def test_fuzzy_match_multiple(self):
        identifier = gene_identifier.BruteForceFuzzyGeneIdentifier(self.gene_dict)
        genes = identifier.identify("ATCGCTCTCTCTGGGAGCCCCCCCGG")
        self.assertEqual({"ct-gene-2", "c-gene-1"}, genes)

