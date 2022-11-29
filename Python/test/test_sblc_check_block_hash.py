"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc

class SimpleBlockchainCheckBlockHashTest(unittest.TestCase):
    """Tests of SimpleBlockchain.check_block_hash method."""

    def test_check_block_hash_correct(self):
        """Test that blcok hash validation works."""
        tested_blc = blc.SimpleBlockchain()
        test_block = tested_blc.make_block([{"Bob": 1, "Alice": -1}])
        tested_blc.check_block_hash(test_block)

    def test_check_block_hash_exception(self):
        """Test that blcok hash validation works."""
        tested_blc = blc.SimpleBlockchain()
        test_block = tested_blc.make_block([{"Bob": 1, "Alice": -1}])
        test_block.hash = "123"

        with self.assertRaises(ValueError):
            tested_blc.check_block_hash(test_block)
