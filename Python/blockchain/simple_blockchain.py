"""Basic example of blockchain with transactions between two users."""
import hashlib
import json
import sys
import typing
import random

import blockchain.structures as my_struct


class SimpleBlockchain(object):
    """Class demonstrating basic blockchain functionality implementation."""

    def __init__(
            self,
            seed: int = 0,
            state: dict[str, int] = {"Alice": 50, "Bob": 50},
            chain: list[my_struct.Block] = []
            ) -> None:
        """Create a new blockchain.
        
        Args:
            seed: The seed for the random generator.
            state: the initial state.
        """
        random.seed(seed)
        self.seed: int = seed
        self.state: dict[str, int] = state
        self.chain: list[my_struct.Block] = chain if chain\
            else [self._make_genesis_block()]
        self.chain_bcp = []
        self.state_bcp = {}

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

    def make_block(self,
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
        transactions_buffer: list[dict[str, int]] = []
        for i in range(amount):
            transactions_buffer.append(self.make_random_transaction())
        return transactions_buffer

    def process_buffer(
            self,
            transactions_buffer: list[dict[str, int]],
            max_block_size: int = 5
            ) -> tuple:
        """Process the transaction buffer and extend the blockchain.
        
        Args:
            transactions_buffer: list of transactions.
            max_block_size: partitioning into blocks.
        """
        accepted: int = 0
        rejects: int = 0
        while len(transactions_buffer) > 0:
            transactions_list: list[dict[str, int]] = []
            while (len(transactions_buffer) > 0) and\
                (len(transactions_list) <= max_block_size):
                transaction = transactions_buffer.pop()
                if self.is_valid_transaction(transaction):
                    transactions_list.append(transaction)
                    self.update_state(transaction)
                    accepted += 1
                else:
                    print("Transaction ignored.")
                    rejects += 1
                    sys.stdout.flush()
                    continue
            self.chain.append(
                self.make_block(transactions_list)
            )
            print(
                f"Processed: {transactions_list}\n"
                f" into block {self.chain[-1].blockContents.blockNumber}")
        print(f"Current blockchain size is now {len(self.chain)}")
        return (accepted, rejects)

    def check_block_hash(self, block: my_struct.Block) -> None:
        """Check the hash of a block and raise an exception if it's invalid.

        Args:
            block: Block to be checked.
        Raises:
            ValueError: if the value of the Hash is not appropriate.
        """
        expected_hash = self.hash_msg(block.blockContents)
        if block.hash != expected_hash:
            raise ValueError(
                "Hash doesn't match the contents of block number: %s",
                block.blockContents.blockNumber
                )

    def check_block_validity(
            self,
            block: my_struct.Block,
            parent: my_struct.Block) -> None:
        """Check the validity of block before applying it to current state.

        Args:
            block: The block that should update the state.
            parent: the last updated block.
        Raises:
            ValueError: If parent hash doesn't check out.
            ValueError: If blockNumber doesn't match the parent blockNumber.
            ValueError: If block hash doesn't match block content.
            ValueError: if there is an invalid transaction in the block.
        """
        parent_nr = parent.blockContents.blockNumber
        parent_hash = parent.hash
        block_nr = block.blockContents.blockNumber

        self.check_block_hash(block)

        if block_nr != (parent_nr + 1):
            raise ValueError(
                f"Block number {block_nr} doesn't match the parent number "
                f"{parent_nr}")

        if block.blockContents.parentHash != parent_hash:
            raise ValueError(f"Parent hash is inaccurate at block {block_nr}")

        for transaction in block.blockContents.transactions:
            if self.is_valid_transaction(transaction):
                # If all checks pass, apply the transaction to current state.
                self.update_state(transaction)
            else:
                raise ValueError(
                    f"Invalid transaction {transaction} in block {block_nr}")

    def load_exported_chain(self, chain_str: str) -> list[my_struct.Block]:
        """Load a chain from an exported string.

        Args:
            chain_str: string representation of the chain.
        Returns:
            A blockchain chain candidate.
        Raises:
            May raise exceptions from json.loads()
        """
        # This is rather hacky implementation due to time contraints.
        loaded = json.loads(json.loads(chain_str))
        return [
            my_struct.Block(
            hash=blc["hash"],
            blockContents=my_struct.BlockContents(*blc["blockContents"])
            ) for blc in loaded]

    def export_chain(self) -> str:
        """Export the current chain in a json string."""
        # This is rather hacky due to time constraints.
        return json.dumps(self.chain.__repr__())

    def import_chain(
            self,
            chain: typing.Union[list[my_struct.Block], str]) -> bool:
        """Check the validity of the chain and it's internal integrity.

        Args:
            chain: Either json string of the chain or python list of blocks.
        Returns:
            True if the chain and state has been updated successfully. 
            False in case of any exceptions.
        """
        if isinstance(chain, str):
            try:
                chain = self.load_exported_chain(chain)
                assert( isinstance(chain, list))
            except Exception as exception:
                print(f"Exception caught: {exception}")
                return False
        elif not isinstance(chain, list):
            print("Incompatible type, chain is not a list!")
            return False
        
        # Backup current state and chain in case of failure.
        self.chain_bcp = self.chain
        self.state_bcp = self.state

        try:
            # Reset current state
            self.state = {}
            for transaction in chain[0].blockContents.transactions:
                self.update_state(transaction)
            self.check_block_hash(chain[0])
            parent = chain[0]

            for block in chain[1:]:
                self.check_block_validity(block, parent)
                parent = block
            
            print("Sucessfully validated all blocks in imported chain.")
            self.chain = chain
            return True
        except Exception as any_except:
            self.chain = self.chain_bcp
            self.state = self.state_bcp
            print(f"Failed to import new chain due to exception: {any_except}")
            return False

    def update_chain(
            self,
            chain_extention: typing.Union[list[my_struct.Block], str]) -> None:
        """Update current chain from received data."""
        if isinstance(chain_extention, str):
            try:
                chain_extention = self.load_exported_chain(chain_extention)
                assert( isinstance(chain_extention, list))
            except Exception as exception:
                print(f"Exception caught: {exception}")
                return False
        elif not isinstance(chain_extention, list):
            print("Incompatible type, chain is not a list!")
            return False
        
        # Backup current state and chain in case of failure.

        for block in chain_extention:
            try:            
                self.check_block_validity(block, self.chain[-1])
                self.chain.append(block)
                print(
                    f"Adding block number: {block.blockContents.blockNumber}"
                )
            except Exception as exc:
                print("Invalid block, trying next block.")

        print(f"Blockchain extended to size: {len(self.chain)}")

