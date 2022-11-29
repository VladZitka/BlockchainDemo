"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc
import blockchain.structures as struct

class SimpleBlockchainCheckBlockValidityTest(unittest.TestCase):
    """Tests of SimpleBlockchain.check_block_validity method."""

    def test_check_block_validity_correct(self):
        """Test that valid block updates state correctly."""
        tested_blc = blc.SimpleBlockchain()
        test_block = tested_blc.make_block([{"Bob": 1, "Alice": -1}])

        tested_blc.check_block_validity(test_block, tested_blc.chain[-1])
        self.assertEqual(tested_blc.state, {"Alice": 49, "Bob": 51})

    def test_check_block_validity_exception_hash(self):
        """Test that invalid block hash throws and doesn't update."""
        tested_blc = blc.SimpleBlockchain()
        expected_state = tested_blc.state
        test_block = tested_blc.make_block([{"Bob": 1, "Alice": -1}])
        test_block.hash = "dafasdf"

        with self.assertRaises(ValueError):
            tested_blc.check_block_validity(test_block, tested_blc.chain[-1])
        self.assertEqual(expected_state, tested_blc.state)

    def test_check_block_validity_exception_block_number(self):
        """Test that invalid block blockNumber throws and doesn't update."""
        tested_blc = blc.SimpleBlockchain()
        expected_state = tested_blc.state
        test_block = tested_blc.make_block([{"Bob": 1, "Alice": -1}])
        test_blc_content = struct.BlockContents(
            blockNumber=1234,
            parentHash=test_block.blockContents.parentHash,
            transactionsCount=test_block.blockContents.transactionsCount,
            transactions=test_block.blockContents.transactions
            )
        test_block.blockContents = test_blc_content

        with self.assertRaises(ValueError):
            tested_blc.check_block_validity(test_block, tested_blc.chain[-1])
        self.assertEqual(expected_state, tested_blc.state)

    def test_check_block_validity_exception_parent_hash(self):
        """Test that invalid block parent hash throws and doesn't update."""
        tested_blc = blc.SimpleBlockchain()
        expected_state = tested_blc.state
        test_block = tested_blc.make_block([{"Bob": 1, "Alice": -1}])
        test_blc_content = struct.BlockContents(
            blockNumber=test_block.blockContents.blockNumber,
            parentHash="hash",
            transactionsCount=test_block.blockContents.transactionsCount,
            transactions=test_block.blockContents.transactions
            )
        test_block.blockContents = test_blc_content

        with self.assertRaises(ValueError):
            tested_blc.check_block_validity(test_block, tested_blc.chain[-1])
        self.assertEqual(expected_state, tested_blc.state)

    def test_check_block_validity_exception_invalid_transaction(self):
        """Test that invalid block tranascions throws and doesn't update."""
        tested_blc = blc.SimpleBlockchain()
        expected_state = tested_blc.state
        test_block = tested_blc.make_block([{"Bob": 11, "Alice": -1}])

        with self.assertRaises(ValueError):
            tested_blc.check_block_validity(test_block, tested_blc.chain[-1])
        self.assertEqual(expected_state, tested_blc.state)
