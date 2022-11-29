"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc


class SimpleBlockchainUpdateStateTest(unittest.TestCase):
    """Tests of SimpleBlockchain.update_state method."""

    def test_update_state_new_user(self):
        """Test that new user is inserted into the state correctly."""
        tested_blc = blc.SimpleBlockchain(state={"bob":0})
        test_transaction = {"alice": 0}
        tested_blc.update_state(test_transaction)

        self.assertTrue("alice" in tested_blc.state.keys())
        self.assertTrue("bob" in tested_blc.state.keys())
        self.assertTrue(tested_blc.state["alice"] == 0)
        self.assertTrue(tested_blc.state["bob"] == 0)

    def test_update_state_update_user(self):
        """Test that single user is updated correctly."""
        tested_blc = blc.SimpleBlockchain(state={"bob": 0, "alice": 1})
        test_trans = {"bob": 1}
        tested_blc.update_state(test_trans)
        self.assertEqual(tested_blc.state["alice"], 1)
        self.assertEqual(tested_blc.state["bob"], 1)

    def test_update_state_update_multiple_users(self):
        """Test that multiple users are inserted correctly."""
        tested_blc = blc.SimpleBlockchain(state={"bob": 0, "alice": 1})
        test_trans = {"bob": 1, "alice": -1}
        tested_blc.update_state(test_trans)
        self.assertEqual(tested_blc.state["alice"], 0)
        self.assertEqual(tested_blc.state["bob"], 1)

    def test_update_state_update_and_insert_users(self):
        """Test that users are updated and inserted correctly."""
        tested_blc = blc.SimpleBlockchain(state={"bob": 0})
        test_trans = {"bob": 1, "alice": 1}
        tested_blc.update_state(test_trans)
        self.assertEqual(tested_blc.state["alice"], 1)
        self.assertEqual(tested_blc.state["bob"], 1)