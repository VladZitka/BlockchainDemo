"""File containing unittests of SimpleBlockchain."""
import unittest

import blockchain.simple_blockchain as blc
import blockchain.structures as struct

class SimpleBlockchainExportChainTest(unittest.TestCase):
    """Tests of SimpleBlockchain.export_chain an load_export_chain method."""

    def test_export_chain(self):
        """Test that chain is exported correctly"""
        tested_blc = blc.SimpleBlockchain(chain=[
            struct.Block(
                "hash",
                struct.BlockContents(0,"bla",1)
                )
            ])
        tested_blc.export_chain()
    
    def test_load_exported_chain(self):
        """Test that chain is exported correctly"""
        tested_blc = blc.SimpleBlockchain(chain=[
            struct.Block(
                "hash",
                struct.BlockContents(0,"bla",1)
                )
            ])
        json = tested_blc.export_chain()
        chain_2 = tested_blc.load_exported_chain(json)

        self.assertEqual(tested_blc.chain, chain_2)

    def test_load_exported_chain_json_exeption(self):
        """Test that chain is exported correctly"""
        tested_blc = blc.SimpleBlockchain(chain=[
            struct.Block(
                "hash",
                struct.BlockContents(0,"bla",1)
                )
            ])
        json = tested_blc.export_chain()
        with self.assertRaises(Exception):
            chain_2 = tested_blc.load_exported_chain(json[1:-1])

