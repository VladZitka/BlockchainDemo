"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc


class SimpleBlockchainProcessTransactionsBufferTest(unittest.TestCase):
    """Tests of SimpleBlockchain.process_transactions_buffer method."""

    def test_process_transactions_buffer_all_ok(self):
        """Test that the correct number of blocks is inserted into chain."""
        tested_blc = blc.SimpleBlockchain()
        test_buffer = tested_blc.make_transactions_buffer(5)

        accepted, rejects = tested_blc.process_transactions_buffer(test_buffer)

        self.assertEqual(accepted, 5)
        self.assertEqual(rejects, 0)
        self.assertEqual(len(tested_blc.chain), 2)
    
    def test_process_transactions_buffer_one_reject(self):
        """Test that the correct number of blocks is inserted into chain."""
        tested_blc = blc.SimpleBlockchain()
        test_buffer = tested_blc.make_transactions_buffer(5)
        test_buffer.append({"blib": 20, "bla": 2})

        accepted, rejects = tested_blc.process_transactions_buffer(
            test_buffer,
            3
            )

        self.assertEqual(accepted, 5)
        self.assertEqual(rejects, 1)
        self.assertEqual(len(tested_blc.chain), 3)