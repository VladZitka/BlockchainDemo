"""Basic example of blockchain with transactions between two users."""
import dataclasses
import hashlib
import json
import sys
import typing
import random

import structures as my_struct


class SimpleBlockchain(object):
    """Class demonstrating basic blockchain functionality implementation."""

    def __init__(
            self,
            seed: int = 0,
            state: dict[str, int] = {"Alice": 50, "Bob": 50},
            ) -> None:
        """Create a new blockchain.
        
        Args:
            seed: The seed for the random generator.
            state: the initial state.
        """
        random.seed(seed)
        self.seed: int = seed
        self.state: dict[str, int] = state
        self.chain: list[my_struct.Block] = [self._make_genesis_block()]
        self.transactions_buffer: list[dict[str, int]] = []

    def _make_genesis_block(self) -> my_struct.Block:
        """Create an initial state of the blockchain."""
        gen_block_contents = my_struct.BlockContents(
            blockNumber=0,
            parentHash=None,
            transactionsCount=1,
            transactions=[self.state]
        )
        return my_struct.Block(
            hash=self.hash_msg(gen_block_contents),
            blockContents=gen_block_contents
        )

    def _make_block(self,
            transactions: list[dict[str, int]]) -> my_struct.Block:
        """Create a new block in the blockchain.

        Args:
            transactions: The list of transactions in the block.
        """
        parent_block: my_struct.Block = self.chain[-1]
        parent_hash = parent_block.hash
        block_number = parent_block.blockContents.blockNumber + 1
        transactions_count = len(transactions)
        block_contents = my_struct.BlockContents(
            blockNumber=block_number,
            parentHash=parent_hash,
            transactionsCount=transactions_count,
            transactions=transactions
        )
        block_hash = self.hash_msg(block_contents)
        return my_struct.Block(block_hash, block_contents)

    def hash_msg(self, msg: typing.Any = "") -> str:
        """Helper fucntion to wrap the hashing algorithm.
        
        Args:
            msg: Data to be hashed.
        Returns: 
            hashed message in string format.
        Raises:

        """
        if not isinstance(msg, str):
            msg = json.dumps(msg, sort_keys=True)

        if sys.version_info.major == 2:
            raise ValueError(
                "Please get into the 21 century and don't use python 2"
                )
        else:
            return hashlib.sha256(str(msg).encode("utf-8")).hexdigest()


    def make_random_transaction(self, max_value: int = 3) -> dict[str: int]:
        """Create a random valid transaction.
        
        Note: Transactions cannot create new money and 
        Args:
            max_value: maximum value of the transaction.
        Returns:
            dict with the valid transaction
        """
        sign: int = int(random.getrandbits(1))*2-1
        amount: int = random.randint(1, max_value)
        alice_pays: int = sign * amount
        bob_pays: int = -1 * alice_pays

        return {'Alice': alice_pays, "Bob": bob_pays}

    def update_state(self, transaction: dict[str, int]) -> None:
        """Update the state of the chain by a transaction.

        Note: This will update the state no matter the validity of the
            transaction.
        Args: 
            transaction: Transaction to be applied.
        """
        for key in transaction.keys():
            if key in self.state.keys():
                self.state[key] += transaction[key]
            else:
                self.state[key] = transaction[key]

    def is_valid_transaction(self, transaction: dict[str, int]) -> bool:
        """Check the validity of the transaction on current state.

        Args:
            transaction: Transaction to be validated.
        Returns: 
            True if transaction is valid.
        """
        # All deposits and withdrawals need to be balanced.
        if sum(transaction.values()) != 0:
            return False
        
        # No transaction may cause an overdraft.
        for key in transaction.keys():
            acc_balance = self.state[key] if key in self.state.keys() else 0
            if (acc_balance < 0):
                return False

        return True

    def make_transactions_buffer(
            self,
            amount: int = 30) -> list[dict[str, int]]:
        """Make a list of transactions."""
        for i in range(amount):
            self.transactions_buffer.append(self.make_random_transaction())

    def process_buffer(self, max_block_size: int = 5) -> None:
        """Process the current transaction buffer"""
        while len(self.transactions_buffer) > 0:
            buffer_start_size = len(self.transactions_buffer)
            transactions_list: list[dict[str, int]] = []
            while (len(self.transactions_buffer) > 0) and\
                (len(transactions_list) < max_block_size):
                transaction = self.transactions_buffer.pop()
                if self.is_valid_transaction(transaction):
                    transactions_list.append(transaction)
                    self.update_state(transaction)
                else:
                    print("Transaction ignored.")
                    sys.stdout.flush()
                    continue
            self.chain.append(
                self._make_block(transactions_list)
            )



if __name__ == "__main__":
    inst1 = SimpleBlockchain()
    inst1.make_transactions_buffer()
    inst1.process_buffer()
    for block in inst1.chain:
        print(block)
    print(inst1.state)

