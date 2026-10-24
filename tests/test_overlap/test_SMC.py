import unittest
from sequenceforge import SimpleMatchingCoefficient


class TestSimpleMatchingCoefficient(unittest.TestCase):
    def setUp(self):
        self.algorithm = SimpleMatchingCoefficient()

    def test_matrix_counts_matches_and_mismatches(self):
        for query, subject, expected in [
            ("A", "B", [[0.0, 1.0]]),
            ("ACGT", "ACGT", [[4.0, 0.0]]),
            ("AAAA", "TTTT", [[0.0, 4.0]]),
            ("aCgT", "ACGA", [[3.0, 1.0]]),
        ]:
            with self.subTest(query=query, subject=subject):
                matrix = self.algorithm.matrix(query, subject)
                self.assertEqual(matrix.shape, (1, 2))
                self.assertEqual(matrix.tolist(), expected)
                self.assertEqual(self.algorithm(query, subject).tolist(), expected)
                self.assertEqual(
                    self.algorithm.matrix(subject, query).tolist(), expected
                )
                self.assertEqual(matrix.sum(), len(query))
                self.assertEqual(
                    matrix[0, 0] / len(query), self.algorithm.similarity(query, subject)
                )
                self.assertEqual(
                    matrix[0, 1] / len(query), self.algorithm.distance(query, subject)
                )

    def test_identical_sequences(self):
        """Identical sequences should return perfect similarity and zero distance"""
        seq = "ACGT"
        self.assertAlmostEqual(self.algorithm.similarity(seq, seq), 1.0)
        self.assertAlmostEqual(self.algorithm.distance(seq, seq), 0.0)
        self.assertAlmostEqual(self.algorithm.normalized_similarity(seq, seq), 1.0)
        self.assertAlmostEqual(self.algorithm.normalized_distance(seq, seq), 0.0)

    def test_half_match(self):
        """50% match should yield 0.5 similarity"""
        query = "AAGG"
        subject = "AATT"
        self.assertAlmostEqual(self.algorithm.similarity(query, subject), 0.5)
        self.assertAlmostEqual(self.algorithm.distance(query, subject), 0.5)

    def test_completely_different(self):
        """No matching characters"""
        query = "AAAA"
        subject = "TTTT"
        self.assertAlmostEqual(self.algorithm.similarity(query, subject), 0.0)
        self.assertAlmostEqual(self.algorithm.distance(query, subject), 1.0)

    def test_empty_sequences(self):
        """Empty sequences should return 0.0 similarity and distance"""
        with self.assertRaises(ValueError):
            self.algorithm.similarity("", "")
        with self.assertRaises(ValueError):
            self.algorithm.distance("", "")
        with self.assertRaises(ValueError):
            self.algorithm.normalized_similarity("", "")
        with self.assertRaises(ValueError):
            self.algorithm.normalized_distance("", "")

    def test_case_insensitivity(self):
        """Matching should be case-insensitive"""
        query = "acgt"
        subject = "ACGT"
        self.assertAlmostEqual(self.algorithm.similarity(query, subject), 1.0)

    def test_symmetry(self):
        """Similarity and distance should be symmetric"""
        a = "ACGT"
        b = "AGGT"
        self.assertAlmostEqual(
            self.algorithm.similarity(a, b), self.algorithm.similarity(b, a)
        )
        self.assertAlmostEqual(
            self.algorithm.distance(a, b), self.algorithm.distance(b, a)
        )

    def test_invalid_length(self):
        """Mismatched sequence lengths should raise IndexError"""
        with self.assertRaises(IndexError):
            self.algorithm.similarity("ACG", "ACGT")

    def test_invalid_type(self):
        """Non-string inputs should raise TypeError inside hamming"""
        with self.assertRaises(TypeError):
            self.algorithm.similarity(["A", "C"], ["A", "C"])


if __name__ == "__main__":
    unittest.main()
