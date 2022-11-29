"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc


class SimpleBlockchainIsValidTransactionTest(unittest.TestCase):
    """Tests of SimpleBlockchain.is_valid_transaction method."""

    def test_is_valid_transaction_true(self):
        """Test that valid transactions are correctly validated."""
        tested_blc = blc.SimpleBlockchain(state={"bob": 0, "alice": 1})
        test_trans = {"bob": 1, "alice": -1}

        self.assertTrue(tested_blc.is_valid_transaction(test_trans))

    def test_is_valid_transaction_false_creating_money(self):
        """Test that valid transactions are correctly validated."""
        tested_blc = blc.SimpleBlockchain(state={"bob": 0, "alice": 1})
        test_trans = {"bob": 1, "alice": 1}

        self.assertFalse(tested_blc.is_valid_transaction(test_trans))

    def test_is_valid_transaction_false_overdraft(self):
        """Test that valid transactions are correctly validated."""
        tested_blc = blc.SimpleBlockchain(state={"bob": 0, "alice": 1})
        test_trans = {"bob": -1, "alice": 1}

        self.assertFalse(tested_blc.is_valid_transaction(test_trans))
