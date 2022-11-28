import dataclasses
import typing


class BlockContents(typing.NamedTuple):  
    """Structure to store block contents.

    Note: Inheritance used in order to avoid problem with JSON serializaitons.
    """
    blockNumber: int = 0
    parentHash: typing.Optional[str] = None
    transactionsCount: int = 1
    transactions: typing.Optional[list[dict[str, int]]] = None

@dataclasses.dataclass
class Block():
    """Structure to store a single block of transactions."""
    hash: str
    blockContents: BlockContents    
