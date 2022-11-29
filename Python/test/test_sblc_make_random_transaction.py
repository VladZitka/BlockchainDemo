"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc


class SimpleBlockchainMakeRandomTransactionTest(unittest.TestCase):
    """Tests of SimpleBlockchain.make_random_transaction method."""

    def test_make_random_transaction(self):
        """Test that the correct transaction is created."""
        tested_blc = blc.SimpleBlockchain()
        actual = tested_blc.make_random_transaction(5)
        self.assertEqual(actual["Alice"], -1*actual["Bob"])
        self.assertTrue(abs(actual["Alice"]) < 5)

        