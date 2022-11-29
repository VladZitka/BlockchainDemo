"""File containing unittests of SimpleBlockchain."""
import unittest
import hashlib

import blockchain.simple_blockchain as blc


class SimpleBlockchainHashMsgTest(unittest.TestCase):
    """Tests of SimpleBlockchain.hash_msg method."""

    def test_hash_msg(self):
        """Test that the correct block is created."""
        tested_blc = blc.SimpleBlockchain()
        test_msg = "abcdefg"
        expected_hash = hashlib.sha256(str("abcdefg").encode("utf-8"))\
            .hexdigest()

        self.assertEqual(tested_blc.hash_msg(test_msg), expected_hash)

    def test_hash_msg_exception(self):
        """Check that hash_msg throws if data is not json serializable"""
        tested_blc = blc.SimpleBlockchain()
        test_msg = [{"a": {"bla", "a"}}]

        with self.assertRaises(Exception):
            tested_blc.hash_msg(test_msg)
