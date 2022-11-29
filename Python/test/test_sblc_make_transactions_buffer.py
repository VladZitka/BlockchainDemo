"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc


class SimpleBlockchainMakeTransactionsBufferTest(unittest.TestCase):
    """Tests of SimpleBlockchain.make_transactions_buffer method."""

    def test_make_transactions_buffer(self):
        """Test that the correct lenght of buffer is generated."""
        tested_blc = blc.SimpleBlockchain()
        self.assertEqual(len(tested_blc.make_transactions_buffer(5)), 5)