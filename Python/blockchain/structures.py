import dataclasses
import typing
import json


class BlockContents(typing.NamedTuple):  
    """Structure to store block contents.

    Note: Inheritance used in order to avoid problem with JSON serializaitons.
    """
    blockNumber: int = 0
    parentHash: typing.Optional[str] = None
    transactionsCount: int = 1
    transactions: typing.Optional[list[dict[str, int]]] = None

    def __repr__(self) -> str:
        return json.dumps(self, sort_keys=True)



@dataclasses.dataclass
class Block():
    """Structure to store a single block of transactions."""
    hash: str
    blockContents: BlockContents  

    def __repr__(self) -> str:
        return json.dumps({
            'hash': self.hash,
            'blockContents': self.blockContents
        },
        sort_keys=True)
